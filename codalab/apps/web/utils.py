import logging
import os
import re
import requests

from django.conf import settings
from django.core.files.storage import get_storage_class

logger = logging.getLogger(__name__)

StorageClass = get_storage_class(settings.DEFAULT_FILE_STORAGE)

if hasattr(settings, 'USE_AWS') and settings.USE_AWS:
    BundleStorage = StorageClass(bucket=settings.AWS_STORAGE_PRIVATE_BUCKET_NAME)
    PublicStorage = StorageClass(bucket=settings.AWS_STORAGE_BUCKET_NAME)
elif hasattr(settings, 'BUNDLE_AZURE_ACCOUNT_NAME') and settings.BUNDLE_AZURE_ACCOUNT_NAME:
    BundleStorage = StorageClass(account_name=settings.BUNDLE_AZURE_ACCOUNT_NAME,
                                 account_key=settings.BUNDLE_AZURE_ACCOUNT_KEY,
                                 azure_container=settings.BUNDLE_AZURE_CONTAINER)

    PublicStorage = StorageClass(account_name=settings.AZURE_ACCOUNT_NAME,
                                 account_key=settings.AZURE_ACCOUNT_KEY,
                                 azure_container=settings.AZURE_CONTAINER)
else:
    # No storage provided, like in a test, let's just do something basic
    BundleStorage = StorageClass()
    PublicStorage = StorageClass()


def clean_html_script(html_content):
    # Finds <script and everything between /script>. No scripts for you.
    return re.sub('(<script)(\s*?\S*?)*?(/script>)', "", unicode(html_content))


def docker_image_clean(image_name):
    if not image_name:
        return ""
    # Remove all excess whitespaces on edges, split on spaces and grab the first word.
    # Wraps in double quotes so bash cannot interpret as an exec
    image_name = '"{}"'.format(image_name.strip().split(' ')[0])
    # Regex acts as a whitelist here. Only alphanumerics and the following symbols are allowed: / . : -.
    # If any not allowed are found, replaced with second argument to sub.
    image_name = re.sub('[^0-9a-zA-Z/.:\-_]+', '', image_name)
    return image_name


def check_bad_scores(score_dict):
    bad_score_count = 0
    bad_scores = list()
    for score in score_dict:
        for subm in score['scores']:
            for i in range(len(subm)):
                if type(subm[i]) is dict:
                    for k, v in subm[i].iteritems():
                        if k == 'values':
                            for result in v:
                                for result_key, result_value in result.iteritems():
                                    if result_value == 'NaN' or result_value == '-':
                                        bad_score_count += 1
                                        bad_scores.append(result)
    return bad_score_count, bad_scores


def _put_blob(url, file_path):
    requests.put(
        url,
        data=open(file_path, 'rb'),
        headers={
            # For Azure but doesn't hurt AWS
            'x-ms-blob-type': 'BlockBlob',
        }
    )


def push_submission_to_leaderboard_if_best(submission, keep_only_best=False):
    from apps.web.models import PhaseLeaderBoard, PhaseLeaderBoardEntry, add_submission_to_leaderboard
    # In this phase get the submission score from the column with the lowest ordering
    score_def = submission.get_default_score_def()
    lb = PhaseLeaderBoard.objects.get(phase=submission.phase)

    # Get our leaderboard entries: Related Submissions should be in our participant's submissions,
    # and the leaderboard should be the one attached to our phase
    entries = PhaseLeaderBoardEntry.objects.filter(result__in=submission.participant.submissions.all(), board=lb)
    submissions = [(entry.result, entry.result.get_default_score()) for entry in entries]
    sorted_list = sorted(submissions, key=lambda x: x[1])
    if sorted_list:
        top_sub, top_score = sorted_list[0]
        score_value = submission.get_default_score()
        if score_def.sorting == 'asc':
            # The last value in ascending is the top score, 1 beats 3
            if score_value <= top_score:
                add_submission_to_leaderboard(submission, keep_only_best)
                logger.info("Force best submission added submission to leaderboard in ascending order "
                            "(submission_id=%s, top_score=%s, score=%s)", submission.id, top_score,
                            score_value)
        elif score_def.sorting == 'desc':
            # The first value in descending is the top score, 3 beats 1
            if score_value >= top_score:
                add_submission_to_leaderboard(submission, keep_only_best)
                logger.info(
                    "Force best submission added submission to leaderboard in descending order "
                    "(submission_id=%s, top_score=%s, score=%s)", submission.id, top_score, score_value)
    else:
        add_submission_to_leaderboard(submission, keep_only_best)
        logger.info(
            "Force best submission added submission: {0} with score: {1} to leaderboard: {2}"
            " because no submission was present".format(
                submission, submission.get_default_score(), lb)
        )


def inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


def s3_key_from_url(url):
    if not url or url == '':
        logger.error("Received an invalid url to convert to a key: {}".format(url))
        return
    # Remove the beginning of the URL (before bucket name) so we just have the path(key) to the file
    key = url.split("{}/".format(settings.AWS_STORAGE_PRIVATE_BUCKET_NAME))[-1]
    # Path could also be in a format <bucket>.<url> so check that as well
    key = key.split("{}.{}/".format(settings.AWS_STORAGE_PRIVATE_BUCKET_NAME, settings.AWS_S3_HOST))[-1]
    return key


def get_competition_size_data(competition):
    data = {
        'id': competition.id,
        'title': competition.title,
        'creator': "{0} ({1})".format(competition.creator.email, competition.creator.username),
        'is_active': competition.is_active,
        'submissions': 0,
        'datasets': 0,
        'dumps': 0,
        'bundle': 0,
    }
    data_file_attrs = [
        'reference_data_organizer_dataset',
        'input_data_organizer_dataset',
        'scoring_program_organizer_dataset',
        'public_data_organizer_dataset',
        'starting_kit_organizer_dataset',
        'ingestion_program_organizer_dataset',
    ]
    keys_to_total = [
        'submissions',
        'datasets',
        'bundle',
        'dumps',
    ]
    for phase in competition.phases.all():
        # submissions
        for submission in phase.submissions.all():
            data['submissions'] += get_submission_size(submission)
        # datasets
        for attr in data_file_attrs:
            dataset = getattr(phase, attr)
            if dataset:
                data['datasets'] += dataset.size
    # bundle
    if competition.bundle:
        data['bundle'] = competition.bundle.size
    # dumps
    if competition.dumps.exists():
        data['dumps'] = sum([dump.size for dump in competition.dumps.all()])
    data['total'] = sum([data[key] for key in keys_to_total])
    return data

def get_submission_size(submission):
    total = 0
    if not os.environ.get('PYTEST'):
        file_attrs = [
            'inputfile',
            'runfile',
            'output_file',
            'private_output_file',
            'stdout_file',
            'stderr_file',
            'history_file',
            'scores_file',
            'coopetition_file',
            'detailed_results_file',
            'prediction_runfile',
            'prediction_output_file',
            'prediction_stdout_file',
            'prediction_stderr_file',
            'ingestion_program_stdout_file',
            'ingestion_program_stderr_file',
        ]
        total += get_filefield_size(submission, 'file', aws_attr='s3_file', s3direct=True)
        for file_attr in file_attrs:
            total += get_filefield_size(submission, file_attr)
    return total

def get_filefield_size(obj, attr, aws_attr=None, s3direct=False):
    size = None
    if settings.USE_AWS and s3direct and aws_attr:
        attr_obj = getattr(obj, aws_attr)
        bucket = BundleStorage.bucket
        # S3DirectFields are stored as text fields with the full url to the key.
        key = s3_key_from_url(attr_obj)
        key_obj = bucket.lookup(key)
        if key_obj:
            size = key_obj.size
    else:
        attr_obj = getattr(obj, attr)
        if attr_obj.name and attr_obj.name != '':
            size = attr_obj.size
    # Always make sure we return at least 0
    return size or 0

def delete_key_from_storage(obj, attr, aws_attr=None, s3direct=False, use_boto_method=True):
    """Helper function to do checks and delete a key from storage. Key is FileField.name"""
    if settings.USE_AWS and (use_boto_method or s3direct):
        if not aws_attr:
            aws_attr = attr
        attr_obj = getattr(obj, aws_attr)
        if s3direct:
            storage = BundleStorage
            key = s3_key_from_url(attr_obj)
        else:
            storage = attr_obj.storage
            key = attr_obj.name
        if key == '' or not key:
            logger.error("Attempt to delete empty key: {}".format(key))
            return
        key_obj = storage.bucket.lookup(key)
        if key_obj:
            if key_obj.exists():
                logger.info("Attempting to delete key: {}".format(key))
                key_obj.delete()
    else:
        attr_obj = getattr(obj, attr)
        storage = attr_obj.storage
        if attr_obj.name and attr_obj.name != '':
            logger.info("Attempting to delete storage file: {}".format(attr_obj.name))
            storage.delete(attr_obj.name)

def storage_recursive_find(storage, dir='', depth=0):
    found_files = []
    if not depth >= 99:
        dirs, files = storage.listdir(dir)
        for file in files:
            found_files.append("{0}/{1}".format(dir, file))
        for new_dir in dirs:
            if dir != '':
                new_files = storage_recursive_find(storage, "{}/{}".format(dir, new_dir), depth+1)
            else:
                new_files = storage_recursive_find(storage, "{}".format(new_dir), depth+1)
            found_files += new_files
    else:
        logger.error("Max recursion reached in recursive storage find!")
    return found_files

def storage_get_total_use(storage):
    total_bytes = 0
    if settings.USE_AWS:
        bucket = storage.bucket
        for key in bucket:
            total_bytes += key.size
    else:
        found_files = set(storage_recursive_find(storage, ''))
        for file_path in found_files:
            total_bytes += storage.size(file_path) or 0
    return float(total_bytes)

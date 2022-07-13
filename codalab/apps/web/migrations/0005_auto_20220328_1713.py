# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-03-28 17:13
from __future__ import unicode_literals

import apps.web.models
import django.core.validators
from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20201113_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='image',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-public'), upload_to=apps.web.models._uuidify('logos'), verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='competitiondefbundle',
            name='config_bundle',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('competition-bundles')),
        ),
        migrations.AlterField(
            model_name='competitiondump',
            name='data_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('competition_dump'), verbose_name='Data file'),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='ingestion_program',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('ingestion_program')),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='input_data',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('phase_input_data_file'), verbose_name='Input Data'),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='max_submission_size',
            field=models.PositiveIntegerField(default=300, validators=[django.core.validators.MaxValueValidator(10000), django.core.validators.MinValueValidator(0)], verbose_name='Max submission size in megabytes. (0 for disabled)'),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='public_data',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('public_data'), verbose_name='Public Data'),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='reference_data',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('phase_reference_data_file'), verbose_name='Reference Data'),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='scoring_program',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('phase_scoring_program_file'), verbose_name='Scoring Program'),
        ),
        migrations.AlterField(
            model_name='competitionphase',
            name='starting_kit',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('starting_kit'), verbose_name='Starting Kit'),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='coopetition_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_coopetition')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='detailed_results_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_detailed_results')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_file_name')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='history_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_history')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='ingestion_program_stderr_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('predict_submission_stderr')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='ingestion_program_stdout_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('predict_submission_stdout')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='inputfile',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_inputfile')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='output_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_output')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='prediction_output_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_prediction_output')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='prediction_runfile',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_prediction_runfile')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='prediction_stderr_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('predict_submission_stderr')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='prediction_stdout_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('predict_submission_stdout')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='private_output_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_private_output')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='runfile',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_runfile')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='scores_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_scores')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='stderr_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_stderr')),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='stdout_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('submission_stdout')),
        ),
        migrations.AlterField(
            model_name='organizerdataset',
            name='data_file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='competition1234-private'), upload_to=apps.web.models._uuidify('dataset_data_file'), verbose_name='Data file'),
        ),
    ]
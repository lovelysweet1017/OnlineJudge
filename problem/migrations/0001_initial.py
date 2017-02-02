# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-31 09:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', utils.models.RichTextField()),
                ('input_description', models.CharField(max_length=10000)),
                ('output_description', models.CharField(max_length=10000)),
                ('samples', models.TextField(blank=True)),
                ('test_case_id', models.CharField(max_length=40)),
                ('hint', utils.models.RichTextField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(blank=True, null=True)),
                ('time_limit', models.IntegerField()),
                ('memory_limit', models.IntegerField()),
                ('spj', models.BooleanField(default=False)),
                ('spj_language', models.IntegerField(blank=True, null=True)),
                ('spj_code', models.TextField(blank=True, null=True)),
                ('spj_version', models.CharField(blank=True, max_length=32, null=True)),
                ('visible', models.BooleanField(default=True)),
                ('total_submit_number', models.IntegerField(default=0)),
                ('total_accepted_number', models.IntegerField(default=0)),
                ('difficulty', models.IntegerField()),
                ('source', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'db_table': 'problem',
            },
        ),
        migrations.CreateModel(
            name='ProblemTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'problem_tag',
            },
        ),
        migrations.CreateModel(
            name='TestCaseScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_case_id', models.CharField(max_length=32)),
                ('score', jsonfield.fields.JSONField()),
            ],
            options={
                'db_table': 'test_case_score',
            },
        ),
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(to='problem.ProblemTag'),
        ),
    ]

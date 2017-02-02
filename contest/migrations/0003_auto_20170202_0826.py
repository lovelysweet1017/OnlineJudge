# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-02 08:26
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0002_auto_20170202_0826'),
        ('contest', '0002_contestannouncement_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestproblem',
            name='difficulty',
            field=models.CharField(default='LOW', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contestproblem',
            name='languages',
            field=jsonfield.fields.JSONField(default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contestproblem',
            name='rule_type',
            field=models.CharField(default='ACM', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contestproblem',
            name='source',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contestproblem',
            name='tags',
            field=models.ManyToManyField(to='problem.ProblemTag'),
        ),
        migrations.AddField(
            model_name='contestproblem',
            name='test_case_score',
            field=jsonfield.fields.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contestproblem',
            name='input_description',
            field=utils.models.RichTextField(),
        ),
        migrations.AlterField(
            model_name='contestproblem',
            name='output_description',
            field=utils.models.RichTextField(),
        ),
        migrations.AlterField(
            model_name='contestproblem',
            name='samples',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='contestproblem',
            name='spj_language',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='contestproblem',
            name='test_case_id',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='contestproblem',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-19 08:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='websiteconfig',
            old_name='website_footer',
            new_name='footer',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-25 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_final1', '0006_subject_scheme_sub_tutorial_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='term',
            field=models.CharField(default=b'odd', max_length=200),
        ),
    ]

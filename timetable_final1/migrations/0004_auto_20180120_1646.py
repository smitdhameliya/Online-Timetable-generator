# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-20 11:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_final1', '0003_auto_20180119_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty_subject',
            name='sub_code',
            field=models.ForeignKey(db_column=b'sub_code', on_delete=django.db.models.deletion.CASCADE, to='timetable_final1.subject'),
        ),
    ]

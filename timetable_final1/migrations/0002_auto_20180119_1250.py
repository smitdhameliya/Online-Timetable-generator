# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-19 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_final1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='classroom_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='lab',
            name='lab_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

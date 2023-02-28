# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-13 07:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_final1', '0011_auto_20180209_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='subject_lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_id', models.ForeignKey(db_column=b'lab_id', on_delete=django.db.models.deletion.CASCADE, to='timetable_final1.lab')),
                ('sub_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_final1.subject')),
            ],
        ),
    ]

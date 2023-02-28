# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-09 09:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_final1', '0010_auto_20180209_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='subject_discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descipline_course_table_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_final1.descipline_course')),
                ('semester_table_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_final1.semester')),
                ('shift_table_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_final1.shift')),
            ],
        ),
        migrations.RemoveField(
            model_name='subject',
            name='descipline_course_table_id',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='semester_table_id',
        ),
        migrations.AddField(
            model_name='subject_discipline',
            name='sub_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_final1.subject'),
        ),
    ]
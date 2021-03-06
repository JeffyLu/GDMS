# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-28 13:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('department', '0001_initial'),
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinfo',
            name='s_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='teacher.TeacherInfo', verbose_name='导师'),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='s_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='department.Year', verbose_name='年级'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-18 08:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarsys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='category',
            field=models.CharField(choices=[(0, 'Basic Score'), (1, 'Academic Score'), (2, 'Athletic Score'), (3, 'Student Affair Score'), (4, 'Research Score')], max_length=30),
        ),
        migrations.AlterField(
            model_name='material',
            name='evidence',
            field=models.ImageField(default=1, upload_to='media'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='category',
            field=models.CharField(choices=[(0, 'National Scholarship'), (1, 'University Scholarship'), (2, 'School Academic Scholarship'), (3, 'School Athletic Scholarship'), (4, 'School Student Affair Scholarship'), (5, 'School Research Scholarship')], max_length=30),
        ),
    ]

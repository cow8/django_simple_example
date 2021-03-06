# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-17 16:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('category', models.CharField(choices=[(0, 'National Scholarship'), (1, 'University Scholarship'), (2, 'School Scholarship')], max_length=30)),
                ('score', models.IntegerField()),
                ('status', models.BooleanField(choices=[(0, '未通过'), (1, '通过')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(null=True)),
                ('evidence', models.ImageField(null=True, upload_to='')),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scholarsys.Achievement')),
            ],
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[(0, 'National Scholarship'), (1, 'University Scholarship'), (2, 'School Scholarship')], max_length=30)),
                ('bonus', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_id', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_id', models.CharField(max_length=20)),
                ('scholarship', models.ManyToManyField(to='scholarsys.Scholarship')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='scholarship',
            name='distributer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scholarsys.Staff'),
        ),
        migrations.AddField(
            model_name='achievement',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scholarsys.Student'),
        ),
    ]

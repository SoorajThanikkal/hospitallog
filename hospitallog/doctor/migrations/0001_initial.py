# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2024-01-23 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='reg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('pid', models.CharField(max_length=10)),
                ('phno', models.IntegerField()),
                ('passw', models.CharField(max_length=30)),
                ('cpassw', models.CharField(max_length=30)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2024-02-21 05:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_drreg'),
    ]

    operations = [
        migrations.AddField(
            model_name='drreg',
            name='dimage',
            field=models.ImageField(default=1, upload_to=b''),
            preserve_default=False,
        ),
    ]

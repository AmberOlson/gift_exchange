# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-31 20:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='name',
            field=models.CharField(default='party', max_length=255),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-05 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0002_party_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='admin',
            field=models.BooleanField(default=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-22 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0002_designs'),
    ]

    operations = [
        migrations.AddField(
            model_name='designs',
            name='cost',
            field=models.IntegerField(max_length=60, null=True),
        ),
    ]

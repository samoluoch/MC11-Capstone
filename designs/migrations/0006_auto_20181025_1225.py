# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-25 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0005_designs_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designs',
            name='cost',
            field=models.IntegerField(default='Design under review', max_length=60),
        ),
    ]
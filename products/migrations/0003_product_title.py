# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20151223_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
    ]

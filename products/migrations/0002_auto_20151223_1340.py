# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 12:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seller',
            old_name='geolocation',
            new_name='address',
        ),
        migrations.AddField(
            model_name='product',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 23, 12, 39, 21, 741253, tzinfo=utc), verbose_name='date created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='sold',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='email',
            field=models.EmailField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seller',
            name='password',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]

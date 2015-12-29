# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20151223_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='id',
        ),
        migrations.AlterField(
            model_name='seller',
            name='user',
            field=models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True),
        ),
    ]

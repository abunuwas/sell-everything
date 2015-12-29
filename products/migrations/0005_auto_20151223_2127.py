# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_auto_20151223_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='email',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='name',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='password',
        ),
        migrations.AddField(
            model_name='seller',
            name='user',
            field=models.OneToOneField(default='', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

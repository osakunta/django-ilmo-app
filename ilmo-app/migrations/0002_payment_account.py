# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django-ilmo-app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='account',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]

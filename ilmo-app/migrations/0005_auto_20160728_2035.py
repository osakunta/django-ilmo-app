# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django-ilmo-app', '0004_auto_20160728_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='receiver',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='thank_you_text',
            field=models.TextField(max_length=5000, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django-ilmo-app', '0003_payment_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='thank_you_text',
            field=models.TextField(default='lalalal', max_length=5000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='due_to',
            field=models.DateField(null=True, blank=True),
        ),
    ]

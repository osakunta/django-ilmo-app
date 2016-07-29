# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django-ilmo-app', '0007_auto_20160728_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='payment',
            field=models.ForeignKey(to='django-ilmo-app.Payment', null=True),
        ),
    ]

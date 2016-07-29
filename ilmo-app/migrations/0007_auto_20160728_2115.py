# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django-ilmo-app', '0006_auto_20160728_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='thank_you_text',
            field=djangocms_text_ckeditor.fields.HTMLField(),
        ),
    ]

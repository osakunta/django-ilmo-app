# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django-ilmo-app', '0005_auto_20160728_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=djangocms_text_ckeditor.fields.HTMLField(),
        ),
    ]

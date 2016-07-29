# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('form_name', models.CharField(max_length=50)),
                ('event_date', models.DateTimeField()),
                ('close_date', models.DateTimeField()),
                ('fb_url', models.URLField(blank=True)),
                ('capacity', models.PositiveIntegerField(null=True, blank=True)),
                ('image_url', models.CharField(max_length=1000, blank=True)),
                ('description', models.TextField(max_length=5000)),
                ('backup', models.BooleanField(verbose_name='Accept backup seats?', default=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventAttendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('attendee_name', models.CharField(max_length=50)),
                ('attendee_email', models.CharField(max_length=50, blank=True)),
                ('attendee_phone', models.CharField(max_length=50, blank=True)),
                ('attendee_gender', models.CharField(max_length=50, blank=True)),
                ('attendee_details', models.CharField(max_length=500, blank=True)),
                ('isbackup', models.BooleanField(verbose_name='Is a backup?', default=False)),
                ('registration_date', models.DateTimeField()),
                ('event', models.ForeignKey(to='django-ilmo-app.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('price', models.PositiveIntegerField(null=True, blank=True)),
                ('method', models.CharField(max_length=100, choices=[('Tilisiirto', 'Tilisiirto'), ('Käteinen', 'Käteinen'), ('Ilmainen', 'Ilmainen'), ('Muu', 'Muu')])),
                ('reference_number', models.PositiveIntegerField(null=True, blank=True)),
                ('special_price_offsets', models.CharField(max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50, blank=True)),
                ('zip_code', models.CharField(max_length=50, blank=True)),
                ('city', models.CharField(max_length=50, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='payment',
            field=models.ForeignKey(blank=True, to='django-ilmo-app.Payment'),
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.ForeignKey(to='django-ilmo-app.Place'),
        ),
    ]

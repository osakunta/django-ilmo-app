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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('form_name', models.CharField(max_length=50)),
                ('event_date', models.DateTimeField()),
                ('close_date', models.DateTimeField()),
                ('fb_url', models.URLField(blank=True)),
                ('capacity', models.PositiveIntegerField(blank=True, null=True)),
                ('image_url', models.CharField(blank=True, max_length=1000)),
                ('description', models.CharField(blank=True, max_length=1000)),
                ('thank_you_text', models.CharField(blank=True, max_length=1000)),
                ('backup', models.BooleanField(verbose_name='Accept backup seats?', default=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventAttendee',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('attendee_name', models.CharField(max_length=50)),
                ('attendee_email', models.CharField(blank=True, max_length=50)),
                ('attendee_phone', models.CharField(blank=True, max_length=50)),
                ('attendee_gender', models.CharField(blank=True, max_length=50)),
                ('attendee_details', models.CharField(blank=True, max_length=500)),
                ('isbackup', models.BooleanField(verbose_name='Is a backup?', default=False)),
                ('registration_date', models.DateTimeField()),
                ('event', models.ForeignKey(to='ilmo_app.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.PositiveIntegerField(blank=True, null=True)),
                ('method', models.CharField(choices=[('Tilisiirto', 'Tilisiirto'), ('Käteinen', 'Käteinen'), ('Ilmainen', 'Ilmainen'), ('Muu', 'Muu')], max_length=100)),
                ('receiver', models.CharField(blank=True, max_length=50)),
                ('reference_number', models.PositiveIntegerField(blank=True, null=True)),
                ('due_to', models.DateField(blank=True, null=True)),
                ('account', models.CharField(blank=True, null=True, max_length=100)),
                ('special_price_offsets', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=50)),
                ('zip_code', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='payment',
            field=models.ForeignKey(to='ilmo_app.Payment', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.ForeignKey(to='ilmo_app.Place'),
        ),
    ]

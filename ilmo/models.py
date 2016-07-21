from django.db import models

# DB MODELS
class Attendee(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50,blank=True)
    email = models.CharField(max_length=50,blank=True)
    other = models.CharField(max_length=500,blank=True)

class Address(models.Model):
    address_name = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    region = models.CharField(max_length=50,blank=True)

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.ForeignKey(Address)

class Event(models.Model):
    name = models.CharField(max_length=50)
    event_date = models.DateTimeField()
    place = models.ForeignKey(Place)
    close_date = models.DateTimeField()
    fb_url = models.URLField(blank=True)
    image_urls = models.CharField(max_length=1000,blank=True)
    description = models.CharField(max_length=5000)

class EventAttendee(models.Model):
    event = models.ForeignKey(Event)
    attendee = models.ForeignKey(Attendee)
    registration_date = models.DateField()

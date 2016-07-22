from django.db import models

# DB MODELS
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50,blank=True)
    zip_code = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=50)
    event_date = models.DateTimeField()
    place = models.ForeignKey(Place)
    close_date = models.DateTimeField()
    fb_url = models.URLField(blank=True)
    image_urls = models.CharField(max_length=1000,blank=True)
    description = models.CharField(max_length=5000)

    def __str__(self):
        return self.name

class EventAttendee(models.Model):
    event = models.ForeignKey(Event)
    attendee_name = models.CharField(max_length=50)
    attendee_email = models.CharField(max_length=50,blank=True)
    attendee_phone = models.CharField(max_length=50,blank=True)
    attendee_details = models.CharField(max_length=500,blank=True)
    registration_date = models.DateField()

    def __str__(self):
        return self.name

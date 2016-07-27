import sys
from django.db import models
from django.utils import timezone

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
    reference = models.CharField(max_length=50,verbose_name="Form to use")
    event_date = models.DateTimeField()
    place = models.ForeignKey(Place)
    close_date = models.DateTimeField()
    fb_url = models.URLField(blank=True)
    capacity = models.PositiveIntegerField()
    image_url = models.CharField(max_length=1000,blank=True)
    description = models.TextField(max_length=5000)
    backup = models.BooleanField(verbose_name="Accept backup seats?",default=True)

    def __str__(self):
        return self.name

    def is_past(self):
        if timezone.now() > self.close_date:
            return True
        return False

    def is_full(self):
        count = EventAttendee.objects.filter(event__id=self.id).count()
        capacity = self.capacity if self.capacity is not None else sys.maxsize()
        if capacity < count:
            return True
        return False

class EventAttendee(models.Model):
    event = models.ForeignKey(Event)
    attendee_name = models.CharField(max_length=50)
    attendee_email = models.CharField(max_length=50,blank=True)
    attendee_phone = models.CharField(max_length=50,blank=True)
    attendee_gender = models.CharField(max_length=50,blank=True)
    attendee_details = models.CharField(max_length=500,blank=True)
    registration_date = models.DateField()

    def __str__(self):
        return self.attendee_name

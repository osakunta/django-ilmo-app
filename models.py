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
    form_name = models.CharField(max_length=50)
    event_date = models.DateTimeField()
    place = models.ForeignKey(Place)
    close_date = models.DateTimeField()
    fb_url = models.URLField(blank=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    reference_number = models.PositiveIntegerField(blank=True, null=True)
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
        capacity = self.capacity if self.capacity is not None else sys.maxsize
        if capacity <= count:
            return True
        return False

class EventAttendee(models.Model):
    event = models.ForeignKey(Event)
    attendee_name = models.CharField(max_length=50)
    attendee_email = models.CharField(max_length=50,blank=True)
    attendee_phone = models.CharField(max_length=50,blank=True)
    attendee_gender = models.CharField(max_length=50,blank=True)
    attendee_details = models.CharField(max_length=500,blank=True)
    isbackup = models.BooleanField(verbose_name="Is a backup?", default=False)
    registration_date = models.DateTimeField()

    def __str__(self):
        return self.attendee_name

    def __get_check_number(self):
        base = self.event.reference_number + self.id
        sum = 0
        a = [7,3,1]
        i = 0
        while base > 0:
            sum += (base % 10) * a[i]
            base /= 10
            i = (i + 1) % 3
        ret = sum % 10
        return 0 if ret == 0 else int(10 - ret)

    def get_reference_number(self):
        r = self.event.reference_number
        if r is None:
            return r
        return r * 10 + self.__get_check_number()
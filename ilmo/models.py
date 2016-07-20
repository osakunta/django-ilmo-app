from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=50)
    event_date = models.DateField()
    close_date = models.DateField()

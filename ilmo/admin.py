from django.contrib import admin
from .models import Event,EventAttendee,Place
from django.http import HttpResponse
import json
import csv
from .utils import export_eventattendees_csv

class EventAdmin(admin.ModelAdmin):
    list_display = ('name','event_date','close_date')

class EventAttendeeAdmin(admin.ModelAdmin):
    actions = [export_eventattendees_csv]
    list_display = ('event','attendee_name','registration_date')
    list_filter = ('registration_date',)
    search_fields = ('event__name',)

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Event,EventAdmin)
admin.site.register(Place,PlaceAdmin)
admin.site.register(EventAttendee,EventAttendeeAdmin)

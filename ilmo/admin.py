from django.contrib import admin
from .models import Event,EventAttendee

class EventAdmin(admin.ModelAdmin):
    list_display = ('name','event_date','close_date')
class EventAttendeeAdmin(admin.ModelAdmin):
    list_display = ('event','attendee_name','registration_date')

admin.site.register(Event,EventAdmin)
admin.site.register(EventAttendee,EventAttendeeAdmin)

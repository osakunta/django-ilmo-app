from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from .models import Event, EventAttendee, Place, Payment
from .utils import export_eventattendees_csv, mark_as_paid
admin.site.disable_action('delete_selected')


class EventAdmin(admin.ModelAdmin):
    actions = [admin.actions.delete_selected]
    list_display = ('name', 'event_date', 'close_date')


class EventAttendeeAdmin(admin.ModelAdmin):
    actions = [export_eventattendees_csv, mark_as_paid, 'delete_model']
    list_display = ('event','attendee_name', 'registration_date', 'isbackup', 'haspaid')
    list_filter = ('registration_date', 'isbackup', 'haspaid')
    search_fields = ('event__name',)

    def delete_model(self, request, resultset):
        for obj in resultset:
            obj.delete()
            if not obj.isbackup:
                try:
                    event = obj.event
                    ea = EventAttendee.objects.filter(event=event, isbackup=True).earliest('registration_date')
                except ObjectDoesNotExist:
                    pass
                else:
                    ea.isbackup = False
                    ea.save()
    delete_model.short_description = "Delete selected Event Attendee"


class PlaceAdmin(admin.ModelAdmin):
    actions = [admin.actions.delete_selected]
    list_display = ('name',)


class PaymentAdmin(admin.ModelAdmin):
    actions = [admin.actions.delete_selected]
    list_display = ('name', 'method')

admin.site.register(Event, EventAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(EventAttendee, EventAttendeeAdmin)
admin.site.register(Payment, PaymentAdmin)

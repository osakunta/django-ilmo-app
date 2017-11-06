from .models import Event, EventAttendee, Place
from .config import *
from django import forms
from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.utils import timezone
import json
import csv


def get_eventattendee_rows(queryset):
    rows = []
    for obj in queryset:
        attendee = {'event': obj.event, 'name': obj.attendee_name,
                    'email': obj.attendee_email, 'phone': obj.attendee_phone}
        try:
            details = json.loads(obj.attendee_details)
        except ValueError:
            details = {}
        attendee.update(details)
        rows.append(attendee)
    return rows


def export_eventattendees_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=osallistujat.csv'
    writer = csv.writer(response, csv.excel, delimiter=';')
    response.write(u'\ufeff'.encode('utf8'))
    rows = get_eventattendee_rows(queryset)
    model_order = ['event', 'name', 'email', 'phone']
    writer.writerow(
        ['event', 'name', 'email', 'phone'] + [smart_str(i) for i in rows[0].keys() if i not in model_order])
    for row in rows:
        r = [row.pop('event'), row.pop('name'), row.pop('email'), row.pop('phone')] + [smart_str(i) for i in
                                                                                       row.values()]
        writer.writerow(r)
    return response


export_eventattendees_csv.short_description = 'Export selected to CSV'


def mark_as_paid(modeladmin, request, queryset):
    queryset.update(haspaid=True)


mark_as_paid.short_description = 'Mark as paid'


def save_event_attendee(event_object, data):
    isfull = event_object.is_full()
    gender = get_gender(data['name'])
    ea = EventAttendee(event=event_object,
                       attendee_name=data.pop('name', 'N/A'),
                       attendee_gender=gender,
                       attendee_email=data.pop('email', 'N/A'),
                       attendee_phone=data.pop('phone', 'N/A'),
                       attendee_details=str(data).replace("'", "\"").replace("False", "\"No\"").replace("True",
                                                                                                        "\"Yes\""),
                       isbackup=isfull,
                       registration_date=timezone.now())
    ea.save()
    return ea


def merge_dicts(*args):
    res = {}
    for dict in args:
        res.update(dict)
    return res


def get_resource(fname):
    return RESOURCE_PATH + fname


def get_gender_lists():
    male_file = open(get_resource('names-male.txt'))
    males = [line.rstrip() for line in male_file]
    male_file.close()
    female_file = open(get_resource('names-female.txt'))
    females = [line.rstrip() for line in female_file]
    female_file.close()
    return males, females


def get_gender(name):
    males, females = get_gender_lists()
    first_name = name.split(" ")[0].lower()
    if first_name in [i.lower() for i in males]:
        return "male"
    elif first_name in [i.lower() for i in females]:
        return "female"
    else:
        return "unknown"


class FieldGenerator:
    formfields = {}

    def __init__(self, fields):
        for field in fields:
            options = self.get_options(field)
            f = getattr(self, "create_field_for_" + field['type'])(field, options)
            self.formfields[field['name']] = f

    @staticmethod
    def get_options(field):
        options = {'label': field['label'], 'required': bool(field.get("required", 0))}
        return options

    @staticmethod
    def create_field_for_text(field, options):
        options['max_length'] = int(field.get("max_length", "50"))
        return forms.CharField(**options)

    @staticmethod
    def create_field_for_email(field, options):
        return forms.EmailField(**options)

    @staticmethod
    def create_field_for_textarea(field, options):
        options['max_length'] = int(field.get("max_value", "9999"))
        return forms.CharField(widget=forms.Textarea, **options)

    @staticmethod
    def create_field_for_integer(field, options):
        options['max_value'] = int(field.get("max_value", "999999999"))
        options['min_value'] = int(field.get("min_value", "-999999999"))
        return forms.IntegerField(**options)

    @staticmethod
    def create_field_for_select(field, options):
        options['choices'] = [(i, i) for i in field['options']]
        return forms.ChoiceField(**options)

    @staticmethod
    def create_field_for_checkbox(field, options):
        return forms.BooleanField(widget=forms.CheckboxInput, **options)

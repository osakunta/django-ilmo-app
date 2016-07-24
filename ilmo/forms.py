from django import forms
from django.forms.util import ErrorList
import json
import os

class FieldGenerator():
    formfields = {}
    def __init__(self, fields):
        for field in fields:
            options = self.get_options(field)
            f = getattr(self, "create_field_for_"+field['type'] )(field, options)
            self.formfields[field['name']] = f

    def get_options(self, field):
        options = {}
        options['label'] = field['label']
        options['required'] = bool(field.get("required", 0))
        return options

    def create_field_for_text(self, field, options):
        options['max_length'] = int(field.get("max_length", "50") )
        return forms.CharField(**options)

    def create_field_for_email(self, field, options):
        return forms.EmailField()

    def create_field_for_textarea(self, field, options):
        options['max_length'] = int(field.get("max_value", "9999") )
        return forms.CharField(widget=forms.Textarea, **options)

    def create_field_for_integer(self, field, options):
        options['max_value'] = int(field.get("max_value", "999999999") )
        options['min_value'] = int(field.get("min_value", "-999999999") )
        return forms.IntegerField(**options)

    def create_field_for_select(self, field, options):
        options['choices']  = field['options']
        return forms.ChoiceField(**options)

    def create_field_for_checkbox(self, field, options):
        return forms.BooleanField(widget=forms.CheckboxInput, **options)

def get_form(event_reference):
    with open('./ilmo-app/ilmo/form_templates/' + event_reference + '.json','r') as template:
        fields = json.load(template)
        fg = FieldGenerator(fields)
        return type('form',(forms.Form,),fg.formfields)

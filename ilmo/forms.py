from django import forms
import json
import os
from .utils import FieldGenerator

def get_form(event_reference):
    with open('./ilmo-app/ilmo/form_templates/' + event_reference + '.json','r') as template:
        fields = json.load(template)
        fg = FieldGenerator(fields)
        return type('form',(forms.Form,),fg.formfields)

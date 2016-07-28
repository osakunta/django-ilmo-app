from django import forms
import json
from . import config
import os
from .utils import FieldGenerator

def get_form(form_name):
    with open(config.FORM_TEMPLATE_PATH + form_name,'r') as template:
        fields = json.load(template)
        fg = FieldGenerator(fields)
        return type('form',(forms.Form,),fg.formfields)

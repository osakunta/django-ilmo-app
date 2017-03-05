from django import forms
import json
from . import config
import os
from .utils import FieldGenerator
import codecs

def get_form(form_name):
    with codecs.open(config.FORM_TEMPLATE_PATH + form_name,'r') as template:
        fields = json.load(template)
        fg = FieldGenerator(fields)
        return type('form',(forms.Form,),fg.formfields)

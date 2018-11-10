from django import forms
import json
from .utils import FieldGenerator
from .models import EventForm


def get_form(url_alias):
    try:
        form = EventForm.objects.filter(url_alias=url_alias).first()

        if not form:
            return None

        fields = json.loads(form.json_content)
        fg = FieldGenerator(fields)
        return type('form', (forms.Form,), fg.formfields)
    except Exception as e:
        return None

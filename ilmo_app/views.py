from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from django.views.decorators.http import require_http_methods
from .models import Event
from .forms import get_form
from .utils import save_event_attendee, merge_dicts, \
    get_event_details_by_url_alias
from .email import send_confirmation_mail


@require_http_methods(['GET'])
def get_all_events(request):
    events = Event.objects.filter(hide=False)
    return render(request,
                  'list.html',
                  dict(event_list=events))


@require_http_methods(['GET'])
def get_coming_events(request):
    return render(request, 'list.html',
                  dict(coming_events=Event.coming_events(),
                       head_past_events=Event.head_past_events(),
                       coming=True))


@require_http_methods(['GET'])
def index(request):
    return render(request,
                  'index.html',
                  dict(content="This is Ilmo App"))


@require_http_methods(['GET'])
def thanks(request):
    return render(request,
                  'thanks.html',
                  dict(content="""
                  Ilmoittautumisesi on vastaanotettu.
                  Vahvistus ilmoittautumisestasi on lähetetty antamaasi sähköpostiosoitteeseen.
                  """))


def registration_form(request, url_alias):
    if request.method == 'GET':
        return get_event_form(request, url_alias)
    elif request.method == 'POST':
        return submit_registration(request, url_alias)


def get_event_form(request, url_alias):
    event_details = get_event_details_by_url_alias(url_alias)
    form = get_form(url_alias)
    if not form:
        raise Http404("Lomaketta ei löydy")
    data = merge_dicts(event_details, dict(form=form))
    return render(request, 'registration_form.html', data)


def submit_registration(request, url_alias):
    event_details = get_event_details_by_url_alias(url_alias)
    form = get_form(url_alias)(request.POST)
    if form.is_valid():
        attendee = save_event_attendee(event_details['event'],
                                       form.cleaned_data)
        if getattr(settings, 'ILMO_EMAIL_CONFIGURED'):
            send_confirmation_mail(event_details['event'],
                                   attendee,
                                   'registration_fi')
        return redirect('thanks')
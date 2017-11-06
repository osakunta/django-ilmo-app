from django.shortcuts import render
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .config import *
from .models import Event, EventAttendee, Place, Payment
from .forms import get_form
from .utils import save_event_attendee, merge_dicts


def get_all_events(request):
    events = Event.objects.filter(hide=False)
    return render(request, 'list.html', {'event_list': events})


def get_coming_events(request):
    coming_events = Event.objects.filter(event_date__gte=timezone.now()).filter(hide=False)
    head_past_events = Event.objects.filter(event_date__lte=timezone.now(),
                                            event_date__gte=timezone.now() - timezone.timedelta(days=14))
    return render(request, 'list.html',
                  {'coming_events': coming_events, 'head_past_events': head_past_events, 'coming': True})


def index(request):
    return render(request, 'index.html', {'content': "This is Ilmo App"})


def thanks(request):
    return render(request, 'index.html', {'content': "Thank you for registration"})


def parse_event_form(request, form_name):
    event_details = get_event_details(form_name)
    if request.method == 'POST':
        form = get_form(form_name)(request.POST)
        if form.is_valid():
            attendee = save_event_attendee(event_details['event'], form.cleaned_data)
            if EMAIL_CONFIGURED:
                msg_html = render_to_string(EMAIL_TEMPLATE_PATH + "registration",
                                            {'attendee': attendee, 'event': event_details['event'],
                                             'payment': event_details['payment']})
                send_mail('Thank you for registration to ' + event_details['event'].name, msg_html, 'sender@mail.com',
                          [attendee.attendee_email], html_message=msg_html, )
            return render(request, 'thanks.html',
                          {'attendee': attendee, 'event': event_details['event'], 'payment': event_details['payment']})
    else:
        form = get_form(form_name)
    data = merge_dicts(event_details, {'form': form})
    return render(request, 'registration_form.html', data)


def get_event_details(form):
    event = Event.objects.get(form_name=form)
    attendees = EventAttendee.objects.filter(event=event.id)
    place = Place.objects.get(id=event.place_id)
    payment = Payment.objects.get(id=event.payment_id)
    attendee_list = []
    for a in attendees:
        attendee = dict(attendee_name=a.attendee_name,
                        isbackup=a.isbackup,
                        reference_number=a.get_reference_number())
        attendee_list.append(attendee)
    return {'event': event, 'attendees': attendee_list, 'place': place, 'payment': payment}
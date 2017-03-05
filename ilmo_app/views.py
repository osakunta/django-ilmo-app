from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .config import *
from .models import Event,EventAttendee,Place,Payment
from .forms import get_form
from .utils import save_event_attendee,merge_dicts

import datetime

def get_all_events(request):
    events = Event.objects.all()
    return render(request,'list.html',{'event_list' : events})

def get_coming_events(request):
    coming_events = Event.objects.filter(event_date__gte=timezone.now())
    head_past_events = Event.objects.filter(event_date__lte=timezone.now(), event_date__gte=timezone.now()-timezone.timedelta(days=14))
    return render(request,'list.html',{'coming_events' : coming_events,'head_past_events': head_past_events, 'coming' : True})

def index(request):
    return render(request,'index.html',{'content' : "This is Ilmo App"})

def thanks(request):
    return render(request,'index.html',{'content' : "Thank you for registration"})

def parse_event_form(request,form_name):
    event_details = get_event_details(form_name)
    if request.method == 'POST':
        form = get_form(form_name)(request.POST)
        if form.is_valid():
            attendee = save_event_attendee(event_details['event'],form.cleaned_data)
            if EMAIL_CONFIGURED:
                msg_html = render_to_string(EMAIL_TEMPLATE_PATH+"registration", {'attendee' : attendee, 'event' : event_details['event'],'payment' : event_details['payment']})
                send_mail('Thank you for registration to ' + event_details['event'].name, msg_html,'sender@mail.com',[attendee.attendee_email],html_message=msg_html,)
            return render(request,'thanks.html',{'attendee' : attendee, 'event' : event_details['event'],'payment' : event_details['payment']})
    else:
        form = get_form(form_name)
    data = merge_dicts(event_details,{'form' : form})
    return render(request, 'registration_form.html',data)

def get_event_details(form):
    event = Event.objects.get(form_name=form)
    attendees = EventAttendee.objects.filter(event=event.id)
    place = Place.objects.get(id=event.place_id)
    payment = Payment.objects.get(id=event.payment_id)
    return {'event' : event, 'attendees' : attendees, 'place' : place, 'payment' : payment}

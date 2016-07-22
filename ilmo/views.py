from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from .models import Event,EventAttendee,Place
from django.http import HttpResponse

def get_all_events(request):
    events = Event.objects.all()
    t = get_template('list.html')
    html = t.render(Context({'event_list' : events}))
    return HttpResponse(html)
def get_event_details(request,event_id):
    event = Event.objects.get(id=event_id)
    attendees = EventAttendee.objects.filter(event=event_id)
    place = Place.objects.get(id=event.place_id)
    t = get_template('event_details.html')
    html = t.render(Context({'event' : event, 'attendees' : attendees, 'place' : place}))
    return HttpResponse(html)
def index(request):
    t = get_template('index.html')
    html = t.render(Context({'content' : 'This is Ilmo App'}))
    return HttpResponse(html)

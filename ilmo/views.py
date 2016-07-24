from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from django.http import HttpResponse

from .models import Event,EventAttendee,Place
from .forms import EventForm

def get_all_events(request):
    events = Event.objects.all()
    t = get_template('list.html')
    html = t.render(Context({'event_list' : events}))
    return HttpResponse(html)

def index(request):
    t = get_template('index.html')
    html = t.render(Context({'content' : 'This is Ilmo App'}))
    return HttpResponse(html)

def parse_event_form(request,event_id):
    event_details = get_event_details(event_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            return HttpResponseDirect('/thanks/')
    else:
        form = EventForm()
    data = merge_dicts(event_details,{'form' : form})
    return render(request, 'registration_form.html',data)

def get_event_details(event_id):
    event = Event.objects.get(id=event_id)
    attendees = EventAttendee.objects.filter(event=event_id)
    place = Place.objects.get(id=event.place_id)
    return {'event' : event, 'attendees' : attendees, 'place' : place}

def merge_dicts(*args):
    res = {}
    for dict in args:
        res.update(dict)
    return res

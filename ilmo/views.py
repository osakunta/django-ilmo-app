from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from ilmo.models import Event
from django.http import HttpResponse

def get_all_events(request):
    events = Event.objects.all()
    t = get_template('list.html')
    html = t.render(Context({'event_list' : events, 'page_title' : 'Ilmo'}))
    return HttpResponse(html)
def index(request):
    t = get_template('list.html')
    return HttpResponse("Welcome to Ilmo - Event Registration")

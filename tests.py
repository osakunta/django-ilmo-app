from django.test import TestCase
from .models import Event,EventAttendee,Place
from datetime import date
EVENT_MOCK = {'name' : 'Event', 'form_name' : 'test_form', 'event_date' : date(2015,1,1), 'capacity' : 2, 'close_date' : date(2014,1,1),'description' : 'empty'}

class EventTestCase(TestCase):
    def setUp(self):
        place = Place.objects.create(name='Place')
        Event.objects.create(**EVENT_MOCK,place=place)

    def test_event_is_past(self):
        event = Event.objects.get(name='Event')
        self.assertEqual(event.is_past(),True)
    def test_event_is_full(self):
        event = Event.objects.get(name='Event')
        self.assertEqual(event.is_full(),False)

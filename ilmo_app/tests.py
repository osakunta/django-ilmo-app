from django.test import TestCase
from .models import Event, EventAttendee, Place, EventCannotAttendException
from datetime import date, timedelta
from django.utils import timezone

PLACE_MOCK = {'name': 'Place'}
EVENT_MOCKS = [
    {'name': 'Event', 'form_name': 'test_form', 'event_date': date(2015, 1, 1), 'capacity': 1,
     'close_date': timezone.now() - timedelta(days=1), 'description': 'empty'},
    {'name': 'Event1', 'form_name': 'test_form', 'event_date': date(2015, 1, 1), 'capacity': 0,
     'close_date': timezone.now() + timedelta(days=1), 'description': 'empty', 'backup': False},
    {'name': 'Event2', 'form_name': 'test_form', 'event_date': date(2015, 1, 1), 'capacity': 1,
     'close_date': timezone.now() + timedelta(days=1), 'description': 'empty'},
    {'name': 'Event3', 'form_name': 'test_form', 'event_date': date(2015, 1, 1), 'capacity': 1,
     'close_date': timezone.now() + timedelta(days=1), 'description': 'empty'}
]


def create_events():
    place = Place.objects.create(**PLACE_MOCK)
    for event in EVENT_MOCKS:
        Event.objects.create(**event, place=place)


def attend_event(event, times=1):
    for i in range(0, times):
        EventAttendee(event=event, attendee_name="Name", registration_date=timezone.now()).save()


class EventTestCase(TestCase):
    def setUp(self):
        create_events()

    def test_event_is_past(self):
        event = Event.objects.get(name='Event')
        self.assertEqual(event.is_past(), True)

    def test_event_is_not_full_with_capacity(self):
        event = Event.objects.get(name='Event')
        self.assertEqual(event.is_full(), False)

    def test_event_is_full_when_capacity_zero(self):
        event = Event.objects.get(name='Event1')
        self.assertEqual(event.is_full(), True)

    def test_event_is_full_when_equals(self):
        event = Event.objects.get(name='Event3')
        capacity = event.capacity
        attend_event(event, times=capacity)
        self.assertEqual(event.is_full(), True)


class EventAttendeeTestCase(TestCase):
    def setUp(self):
        create_events()

    def test_can_register_to_empty_event_with_capacity(self):
        event = Event.objects.get(name='Event3')
        attend_event(event)
        self.assertTrue

    def test_can_register_to_full_event_accepting_backups(self):
        event = Event.objects.get(name='Event2')
        times = 2
        attend_event(event, times=times)
        self.assertTrue(EventAttendee.objects.filter(event=event).count(), times)

    def test_cannot_register_to_full_event_not_accepting_backups(self):
        event = Event.objects.get(name='Event1')
        with self.assertRaises(EventCannotAttendException) as are:
            attend_event(event)

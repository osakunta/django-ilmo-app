from django.test import TestCase
from ilmo_app.models import Event, EventAttendee, Place, Payment
from ilmo_app.models.exceptions import EventCannotAttendException, InvalidPaymentMethod
from datetime import timedelta
from django.utils import timezone
import uuid
import json


class TestPaymentModel(TestCase):
    def test_fails_with_invalid_choice(self):
        with self.assertRaises(InvalidPaymentMethod):
            Payment(name='Payment X',
                    price=100,
                    method='Foo').save()


class TestEvent(TestCase):
    def setUp(self):
        _create_events()

    def test_event_is_past(self):
        event = Event.objects.get(name='EventInPast')
        self.assertTrue(event.is_past())

    def test_event_in_future_is_not_past(self):
        event = Event.objects.get(name='EventInFuture')
        self.assertFalse(event.is_past())

    def test_event_is_not_open_yet(self):
        event = Event.objects.get(name='EventWithOpenDateInFuture')
        self.assertFalse(event.is_open_for_registration())

    def test_event_open_for_registration(self):
        event = Event.objects.get(name='EventWithPastOpenDate')
        self.assertTrue(event.is_open_for_registration())

    def test_event_is_not_full_with_capacity(self):
        event = Event.objects.get(name='EventInPast')
        self.assertTrue(event.capacity > 0)
        self.assertFalse(event.is_full())

    def test_event_is_full_when_capacity_zero(self):
        event = Event.objects.get(name='EventWithZeroCapacity')
        self.assertEquals(event.capacity, 0)
        self.assertTrue(event.is_full())

    def test_cannot_attend_past_event(self):
        event = Event.objects.get(name='EventInPast')
        with self.assertRaises(EventCannotAttendException):
            _attend_event(event, times=1)

    def test_cannot_attend_full_event_without_backup(self):
        event = Event.objects.get(name='EventInFuture')
        event.backup = False
        event.save()

        _attend_event(event, event.capacity)
        with self.assertRaises(EventCannotAttendException):
            _attend_event(event, times=1)

    def test_can_register_to_full_event_accepting_backups(self):
        event = Event.objects.get(name='EventInFuture')
        _attend_event(event, times=event.capacity)
        event.refresh_from_db()
        self.assertTrue(event.is_full())
        _attend_event(event, times=1)

    def test_can_attend_future_event(self):
        event = Event.objects.get(name='EventInFuture')
        self.assertEquals(len(EventAttendee.objects.all()), 0)
        _attend_event(event, times=1)
        self.assertEquals(len(EventAttendee.objects.all()), 1)

    def test_event_is_full_when_number_of_attendees_equals_capacity(self):
        event = Event.objects.get(name='EventInFuture')
        capacity = event.capacity
        _attend_event(event, times=capacity)
        self.assertTrue(event.is_full())


class EventAttendeeTestCase(TestCase):
    def setUp(self):
        _create_events()

    def test_event_attendee_gets_base_price(self):
        payment = Payment(method='Muu', price=10)
        payment.save()
        event = Event.objects.get(name='EventInFuture')
        event.payment = payment
        event.save()

        attendee = EventAttendee(attendee_name='Foo Bar',
                                 event=event,
                                 registration_date=timezone.now())
        attendee.save()
        self.assertEquals(payment.price, attendee.get_price())

    def test_event_attendee_gets_discount_based_on_model_detail_field(self):
        discount = -2
        payment = Payment(method='Muu', price=10, special_price_offsets=json.dumps(dict(age_group=dict(youth=discount))))
        payment.save()
        event = Event.objects.get(name='EventInFuture')
        event.payment = payment
        event.save()

        attendee = EventAttendee(attendee_name='Foo',
                                 event=event,
                                 registration_date=timezone.now(),
                                 attendee_details=json.dumps(dict(age_group="youth")))
        attendee.save()
        self.assertEquals(payment.price + discount, attendee.get_price())


def _create_events():
    place = {'name': 'Place'}

    future_dt = timezone.now() + timedelta(days=1)
    past_dt = timezone.now() - timedelta(days=1)

    events = [
        {'name': 'EventInPast', 'event_date': past_dt, 'capacity': 1, 'close_date': past_dt},
        {'name': 'EventWithZeroCapacity', 'event_date': future_dt, 'capacity': 0, 'close_date': future_dt, 'backup': False},
        {'name': 'EventInFuture', 'event_date': future_dt, 'capacity': 1, 'close_date': future_dt},
        {'name': 'EventWithOpenDateInFuture', 'event_date': future_dt, 'capacity': 1, 'close_date': future_dt, 'open_date': future_dt},
        {'name': 'EventWithPastOpenDate', 'event_date': future_dt, 'capacity': 1, 'close_date': future_dt, 'open_date': past_dt}
    ]

    place = Place.objects.create(**place)
    for event in events:
        Event.objects.create(**event, description='foo', url_alias=uuid.uuid4(), place=place)


def _attend_event(event, times=1):
    for i in range(0, times):
        EventAttendee(event=event, attendee_name="Name", registration_date=timezone.now()).save()

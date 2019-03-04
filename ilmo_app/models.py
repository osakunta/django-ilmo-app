import sys
import json
from django.db import models
from django.utils import timezone
from djangocms_text_ckeditor.fields import HTMLField


class EventCannotAttendException(Exception):
    pass


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    _payment_choices = ["Tilisiirto", "Käteinen", "Ilmainen", "Muu"]

    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField(blank=True, null=True)
    method = models.CharField(choices=[(i, i) for i in _payment_choices], max_length=100)
    receiver = models.CharField(max_length=50, blank=True)
    reference_number = models.PositiveIntegerField(blank=True, null=True)
    due_to = models.DateField(blank=True, null=True)
    account = models.CharField(blank=True, null=True, max_length=100)
    special_price_offsets = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class EventForm(models.Model):
    name = models.CharField(max_length=50)
    json_content = models.CharField(max_length=4096)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Tapahtuman nimi')
    url_alias = models.CharField(max_length=50,
                                 unique=True,
                                 verbose_name='URL-nimi')
    form = models.ForeignKey(EventForm,
                             null=True,
                             verbose_name='Lomake')
    event_date = models.DateTimeField(verbose_name='Tapahtuman ajankohta')
    place = models.ForeignKey(Place, verbose_name='Tapahtuman paikka')
    open_date = models.DateTimeField(verbose_name='Lomakkeen alkamisaika',
                                     null=True,
                                     blank=True,
                                     default=timezone.datetime(2018, 1, 1))
    close_date = models.DateTimeField(verbose_name='Lomakkeen sulkemisaika')
    fb_url = models.URLField(blank=True, verbose_name='Linkki Facebook-tapahtumaan')
    capacity = models.PositiveIntegerField(blank=True,
                                           null=True,
                                           verbose_name='Osallistujien enimmäismäärä')
    payment = models.ForeignKey(Payment,
                                null=True,
                                blank=True,
                                verbose_name='Maksutapa')
    image_url = models.CharField(max_length=1000,
                                 blank=True,
                                 verbose_name='Linkki otsakekuvaan')
    description = HTMLField(verbose_name='Tapahtumakuvaus')
    thank_you_text = HTMLField(verbose_name='Teksti, joka näytetään lomakkeen lähettämisen jälkeen')
    backup = models.BooleanField(verbose_name='Tapahtumaan voi osallistua varasijalle?', default=True)
    hide = models.BooleanField(verbose_name='Piilota tapahtuma listauksesta?', default=False)

    def __str__(self):
        return self.name

    def is_yet_open_for_registration(self):
        return not self.open_date or self.open_date < timezone.now()

    def is_past(self):
        if timezone.now() > self.close_date:
            return True
        return False

    def is_full(self):
        count = EventAttendee.objects.filter(event__id=self.id).count()
        capacity = self.capacity if self.capacity is not None else sys.maxsize
        if capacity <= count:
            return True
        return False

    def is_hide(self):
        return self.hide or self.open_date < timezone.now()

    @classmethod
    def coming_events(cls):
        return Event.objects.filter(event_date__gte=timezone.now()).filter(hide=False)

    @classmethod
    def head_past_events(cls, days=14):
        return Event.objects.filter(event_date__lte=timezone.now(),
                                    event_date__gte=timezone.now() - timezone.timedelta(days=days))


class EventAttendee(models.Model):
    event = models.ForeignKey(Event)
    attendee_name = models.CharField(max_length=100)
    attendee_email = models.CharField(max_length=50, blank=True)
    attendee_phone = models.CharField(max_length=50, blank=True)
    attendee_gender = models.CharField(max_length=50, blank=True)
    attendee_details = models.CharField(max_length=10000, blank=True)
    isbackup = models.BooleanField(verbose_name="Is a backup?", default=False)
    registration_date = models.DateTimeField()
    haspaid = models.BooleanField(verbose_name="Has paid?", default=False)

    def __str__(self):
        return self.attendee_name

    def save(self, *args, **kwargs):
        if self.event.is_full() and not self.event.backup:
            raise EventCannotAttendException("Event is full and no backups taken")
        elif self.event.close_date < timezone.now():
            raise EventCannotAttendException("Event registration time has past")
        super(EventAttendee, self).save(*args, **kwargs)

    def get_price(self):
        price = self.event.payment.price
        ep = Payment.objects.get(event=self.event)
        try:
            special_prices_map = json.loads(ep.special_price_offsets)
        except ValueError:
            return price
        else:
            attendee_details_map = json.loads(self.attendee_details)
            for name, offsets in special_prices_map.items():
                price += offsets.get(attendee_details_map.get(name), 0)
            return price

    @staticmethod
    def __get_check_number(base):
        base = int(base)
        sum = 0
        a = [7, 3, 1]
        i = 0
        while base > 0:
            sum += (base % 10) * a[i]
            base = int(base / 10)
            i = (i + 1) % 3
        ret = sum % 10
        return 0 if ret == 0 else int(10 - ret)

    def get_reference_number(self):
        if not self.event.payment:
            return None
        r = self.event.payment.reference_number
        if r is None:
            return r
        r += self.id
        return r * 10 + self.__get_check_number(r)

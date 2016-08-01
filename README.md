[![Build Status](https://travis-ci.org/mremes/django-ilmo-app.svg?branch=master)](https://travis-ci.org/mremes/django-ilmo-app) [![Coverage Status](https://coveralls.io/repos/github/mremes/django-ilmo-app/badge.svg?branch=master)](https://coveralls.io/github/mremes/django-ilmo-app?branch=master)
# Ilmo App
Project is a lightweight event registration & reporting application for Django Framework.

As it stands, the implemented MVC pattern is currently made on an ad hoc basis but it's possible to reuse it as such or with user's own domain-specific modifications.

## Usage
To test out functionalities (currently tested with Python 3.5 and Django 1.8.13):

1) Create a virtual environment with Python 3.5
```
virtualenv -p /usr/bin/python3.5 envname
```
2) Activate virtual environment
```
source envname/bin/activate
```
3) Install django (at least) package via pip
```
pip install "django=1.8.13"
```
4) Edit ```TIME_ZONE``` variable in ```mysite/settings.py``` to match your time zone

5) Run the server
```
python manage.py runserver
```
6) Open Ilmo welcome page in browser:
```
http://localhost:8000/ilmo
```
## Models

### Place
Represents a place with **name**, address, zip code and city properties as attributes
### Payment
Represents a payment option (foreign key to an Event object) with **name**, price, **method**, receiver, reference number, due to date, special price offsets and account number as attributes. Price field is currently an integer field. There is no validation for reference number, due to date, special price offsets (correct json format) or account number attributes.

'Special price offsets' is a special attribute using which price can be affected depending on form fields and inputs. It requires special data format to get it working:

```
{'form_field1' : {'form_input1' : price_offset_integer1, 'form_input2' : price_offset_integer2, ...}, 'form_field2' : {...}, ...}
```

### Event
Represents an event. Attributes: **name**, **form filename**, **event date**, **Place object**, **registration closing date**, URL to Facebook event page, capacity, Payment object, url to an image, event description, thank you text and backup boolean as attributes.


### EventAttendee
TODO

Objects of these models can be saved either using CLI (Django shell or manual database inserts) or admin interface

## Views and templates
With the current templates
- list all events
- show event registration page containing event details and registration form
- thank you page containing payment details of the event and event's thank you message after registration

## Forms
Forms for populating EventAttendee table are done with .json templates in /form_templates. The json keys which are defined in the EventAttendee model are saved into model and additional fields are saved under attendee_details key as a string representation of a Python dictionary. Thus only keys defined explicitly in the model can be used for querying data.

Currently supporting following field types: text, email, textarea, integer, select, checkbox

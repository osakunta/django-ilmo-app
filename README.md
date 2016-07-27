# Ilmo App
Project is a lightweight event registration & reporting application for Django Framework.

As it stands, the implemented MVC pattern is currently made on an ad hoc basis but it's possible to reuse it as such or with user's own domain-specific modifications.

## Usage
1) Clone the repository into root of your current project:
```
git clone https://github.com/mremes/django-ilmo-app.git
```

2) Add 'ilmo-app.ilmo' to INSTALLED_APPS list in your_site/settings.py

3) Add this line to your your_site/urls.py (see more on Django's URL scheme [here](https://docs.djangoproject.com/ja/1.9/topics/http/urls/))
```
url(r'^path_to_app/',include('ilmo-app.ilmo.urls',namespace='ilmo'))
```

4) Migrate the models to the database you are using with:
```
python manage.py makemigrations ilmo
python manage.py sqlmigrate ilmo 0001
python manage.py migrate
```

5) Run your server and go to the app root and you should get a HTTP response:
```
This is Ilmo App
```

## Models
- Place
- Event
- EventAttendee

Objects of these models can be saved either using CLI (django shell or manual database inserts) or admin interface

## Views
With the current views you can list all events, show event details and register for event

## Templates
There are sample templates in ilmo/templates folder that can be used for testing out

## Forms
Forms for populating EventAttendee table are done with .json templates in /ilmo/form_templates. The json keys which are defined in the EventAttendee model are saved into model and additional fields are saved under attendee_details key as a string representation of a Python dictionary. Thus only keys defined explicitly in the model can be used for querying data.


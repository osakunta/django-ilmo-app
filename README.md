[![Build Status](https://travis-ci.org/osakunta/django-ilmo-app.svg?branch=master)](https://travis-ci.org/osakunta/django-ilmo-app)

## Ilmo app
Django app for event registration and event management

## Form creation

Registration forms for events are created with a JSON form template.
```
[
  {"type": "text","name": "name", "label": "Nimi", "required" : 1},
  {"type": "email","name": "email","label": "Sähköposti", "required" : 1},
  {"type": "radioselect", "name": "status", "label": "Olen", "options": ["Fuksi","Civis","Seniori"], "required" : 1},
  {"type": "text", "name": "org", "label": "Minkä tai mistä, jos ei SatO"}
]
```

Templates are located in `templates/form` directory. These forms are used in the creation of an Event in the admin section by inputting the full file name into the respective input field.

### Properties

#### Required properties
* `type` – defines type of the form field. Supported values:
  - `text` – text field
  - `integer` – validated integer-only field
  - `email` - validated email field
  - `textarea` – text area field for texts that are 9999 characters long
  - `select` – options listing with a drop down list
  - `radioselect` – options listing with radio buttons
  - `checkbox` – check box field
* `name` – name of the field in the database / exported attendee listing
* `label` – text label presented in the UI

#### Optional properties
* `required` – value is 1 if required
* `options` – list of options in an array if `type` is `select` or `radioselect`

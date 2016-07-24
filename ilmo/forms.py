from django import forms

class EventForm(forms.Form):
    name = forms.CharField(label='Name',max_length=50)
    email = forms.CharField(label='Email',max_length=100)
    phone = forms.CharField(label='Phone',max_length=15)
    

from django import forms
from django.contrib.auth.forms import UserCreationForm

class VotreFormulaire(forms.Form):
    city = forms.CharField(label='City', max_length=100)
    address = forms.CharField(label='Address', max_length=255)

class VotreUserCreationForm(UserCreationForm):
    city = forms.CharField(label='City', max_length=100)
    address = forms.CharField(label='Address', max_length=255)
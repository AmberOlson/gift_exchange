from django import forms
from django.forms import ModelForm
from exchange.models import Party, Participant
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _


class PartyCreateForm(forms.Form):
    name = forms.CharField(label='Name:', max_length=100)


class ParticipantCreateForm(forms.Form):
    participant = forms.EmailField(label="Email:", max_length=100)


class SignUpForm(forms.Form):
    username = forms.CharField(label="Name:", max_length=100)
    email = forms.EmailField(label="Email:", max_length=100)
    password = forms.CharField(label="Password:", max_length=100)


class UpDateParty(forms.ModelForm):

    class Meta:
        model = Party
        fields = ['name']

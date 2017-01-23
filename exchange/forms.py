from django import forms
from django.forms import ModelForm
from exchange.models import Party


class PartyCreateForm(forms.Form):
    name = forms.CharField(label='Name:', max_length=100)


class ParticipantCreateForm(forms.Form):
    participant = forms.EmailField(label="Email:", max_length=100)


class ParticipanJoinForm(forms.Form):
    status = forms.CharField(initial="Joined", max_length=100)


class ParticipanLeavingForm(forms.Form):
    status = forms.CharField(initial="Left", max_length=100)


class SignUpForm(forms.Form):
    username = forms.CharField(label="Name:", max_length=100)
    email = forms.EmailField(label="Email:", max_length=100)
    password = forms.CharField(label="Password:", max_length=100)


class UpDateParty(forms.ModelForm):

    class Meta:
        model = Party
        fields = ['name']

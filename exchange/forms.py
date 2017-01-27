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
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label="Password:")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label="Verify Password:")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class UpDateParty(forms.ModelForm):

    class Meta:
        model = Party
        fields = ['name']

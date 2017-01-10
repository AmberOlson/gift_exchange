from django import forms

class PartyCreateForm(forms.Form):
    name = forms.CharField(label='Name:', max_length=100)

class ParticipantCreateForm(forms.Form):
    participant = forms.EmailField(label="Email:", max_length=100)

class SignUpForm(forms.Form):
    username = forms.CharField(label="Name:", max_length=100)
    email = forms.EmailField(label="Email:", max_length=100)
    password = forms.CharField(label="Password:", max_length=100)

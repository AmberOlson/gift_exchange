from django import forms

class PartyCreateForm(forms.Form):
    name = forms.CharField(label='Name:', max_length=100)

class ParticipantCreateForm(forms.Form):
    participant = forms.IntegerField(label="ID:")

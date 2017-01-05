from django import forms

class PartyCreateForm(forms.Form):
    name = forms.CharField(label='Name:', max_length=100)

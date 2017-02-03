
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from exchange.forms import PartyCreateForm, ParticipantCreateForm, SignUpForm, UpDateParty
from exchange.models import Party, Participant, Exchange
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from exchange.domain import start_exchange
from exchange.mail import sendmail
from exchange.signup import signup, match_user_to_party
from django.db import IntegrityError


class ExchangeView(LoginRequiredMixin, TemplateView):

    login_url = '/login/'

    def post(self, request, **kwargs):
        party = get_object_or_404(Party, pk=self.kwargs.get('pk'))
        start_exchange(party)
        return redirect('party_list')

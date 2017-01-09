from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from exchange.forms import PartyCreateForm, ParticipantCreateForm
from exchange.models import Party, Participant, Exchange
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from exchange.domain import start_exchange


class PartyListView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "parties.html"

    def get_context_data(self):
        context = {'cat': 'candy', 'parties': Party.objects.all()}
        return context


class PartyView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "party_view.html"

    def get_context_data(self, **kwargs):
        users = User.objects.all()
        participants = Participant.objects.filter(party=self.kwargs.get('pk'))
        exchanges = Exchange.objects.filter(party=self.kwargs.get('pk'))
        party = get_object_or_404(Party, pk=self.kwargs.get('pk'))
        context = {'party': party, 'users': users, 'participants': participants, 'exchanges': exchanges}
        return context


class PartyCreateView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "party_create.html"

    def get_context_data(self):
        form = PartyCreateForm(self.request.POST or None)  # instance= None
        context = {'form': form}
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context["form"].is_valid():
            print 'yes done'
            Party.objects.create(name=context['form'].cleaned_data['name'])
            return redirect('party_list')
        return super(TemplateView, self).render_to_response(context)


class ParticipantCreateView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "party_participant_create.html"

    def get_context_data(self, **kwargs):
        party = get_object_or_404(Party, pk=self.kwargs.get('pk'))
        form = ParticipantCreateForm(self.request.POST or None)
        context = {'form': form, 'party': party}
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        party = get_object_or_404(Party, pk=self.kwargs.get('pk'))
        if context["form"].is_valid():
            print 'yes done'
            user = User.objects.get(email=context['form'].cleaned_data['participant'])
            Participant.objects.create(user=user, party=party)
            return redirect('party_list')
        return super(ParticipantCreateView, self).render_to_response(context)


class ExchangeView(LoginRequiredMixin, TemplateView):

    login_url = '/login/'

    def post(self, request, **kwargs):
        party = get_object_or_404(Party, pk=self.kwargs.get('pk'))
        start_exchange(party)
        return redirect('party_list')

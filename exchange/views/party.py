
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


class PartyListView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "parties.html"

    def get_context_data(self):
        parties = Party.objects.filter(participant__user=self.request.user)
        context = {'parties': parties}
        return context


class PartyView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "party_view.html"

    def get_context_data(self, **kwargs):
        users = User.objects.all()
        participants = Participant.objects.filter(party=self.kwargs.get('pk'))
        exchanges = Exchange.objects.filter(party=self.kwargs.get('pk'))
        party = get_object_or_404(Party, pk=self.kwargs.get('pk'))
        admin = Participant.objects.filter(party=party, user=self.request.user, admin=True)
        current_user = Participant.objects.filter(party=party, user=self.request.user)
        try:
            your_exchange = Exchange.objects.get(party=party, giver=current_user)
        except Exchange.DoesNotExist:
            your_exchange = None

        form = UpDateParty(self.request.POST or None, instance=party)

        context = {
            'party': party,
            'users': users,
            'participants': participants,
            'exchanges': exchanges,
            'form': form,
            'your_exchange': your_exchange,
            'admin': admin
        }
        return context

    def post(self, request, **kwargs):
        context = self.get_context_data()
        if context["form"].is_valid():
            context["form"].save()
            return redirect('party_list')
        return super(TemplateView, self).render_to_response(context)


class PartyDelete(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "party_delete.html"

    def get_context_data(self, **kwargs):
        party = get_object_or_404(Party, pk=self.kwargs.get('pk'))
        context = {'party': party}
        return context

    def post(self, request, **kwargs):
        party = get_object_or_404(Party, pk=self.kwargs.get('pk'))
        party.delete()
        return redirect('party_list')


class PartyCreateView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "party_create.html"

    def get_context_data(self):
        form = PartyCreateForm(self.request.POST or None)
        context = {'form': form}
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context["form"].is_valid():
            party = Party.objects.create(name=context['form'].cleaned_data['name'])
            Participant.objects.create(party=party, user=request.user, admin=True)
            return redirect('party_list')
        return super(TemplateView, self).render_to_response(context)

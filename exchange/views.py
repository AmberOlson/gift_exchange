from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from exchange.forms import PartyCreateForm, ParticipantCreateForm, SignUpForm, UpDateParty
from exchange.models import Party, Participant, Exchange
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from exchange.domain import start_exchange
from exchange.mail import sendmail


class SignUpView(TemplateView):
        login_url = '/login/'
        template_name = "signup.html"

        def get_context_data(self):
            form = SignUpForm(self.request.POST or None)  # instance= None
            context = {'form': form}
            return context

        def post(self, request):
            context = self.get_context_data()
            if context["form"].is_valid():
                User.objects.create_user(username=context['form'].cleaned_data['username'], email=context['form'].cleaned_data['email'], password=context['form'].cleaned_data['password'])
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                return redirect('party_list')
            return super(TemplateView, self).render_to_response(context)


class PartyListView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "parties.html"

    def get_context_data(self):
        # parties = Party.objects.all()
        parties = Party.objects.filter(participant__user=self.request.user)
        context = {'cat': 'candy', 'parties': parties}
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
            # 'participants': party.participant_set.all(),
            # 'exchanges': party.exchange_set.all(),
            'participants': participants,
            'exchanges': exchanges,
            'form': form,
            # 'current_user': current_user,
            'your_exchange': your_exchange,
            'admin': admin
        }
        # import pdb; pdb.set_trace()
        return context

    def post(self, request, **kwargs):
        # instance = Party.objects.get(id=self.kwargs.get('pk'))
        # form = UpDateParty(request.POST or None, instance=instance)
        context = self.get_context_data()
        if context["form"].is_valid():
            context["form"].save()
            return redirect('party_list')
        return direct_to_template(request, 'my_template.html', {'form': form})


class PartyDelete(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "party_delete.html"

    def get_context_data(self,  **kwargs):
        party = get_object_or_404(Party, pk=self.kwargs.get('pk'))
        context = {'party': party}
        return context

    def post(self, request,  **kwargs):
        party = get_object_or_404(Party, pk=self.kwargs.get('pk')).delete()
        return redirect('party_list')
        # party.delete()

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
            party = Party.objects.create(name=context['form'].cleaned_data['name'])
            Participant.objects.create(party=party, user=request.user, admin=True)
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
            try:
                user = User.objects.get(email=context['form'].cleaned_data['participant'])
                Participant.objects.create(user=user, party=party)
                return redirect('party_list')
            except User.DoesNotExist:
                pass

            sendmail(context['form'].cleaned_data['participant'])
            return redirect('party_list')
        return super(ParticipantCreateView, self).render_to_response(context)

class ParticipantEditView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'

    def post(self, request, **kwargs):
        participant = Participant.objects.get(party=self.kwargs.get('pk'), user=request.user)
        participant.status = "Joined"
        participant.save()
        return redirect('party_list')

class ExchangeView(LoginRequiredMixin, TemplateView):

    login_url = '/login/'

    def post(self, request, **kwargs):
        party = get_object_or_404(Party, pk=self.kwargs.get('pk'))
        start_exchange(party)
        return redirect('party_list')

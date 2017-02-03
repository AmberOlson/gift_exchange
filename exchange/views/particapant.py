
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
                participant = Participant.objects.create(party=party)
                sendmail(context['form'].cleaned_data['participant'], participant)
                return redirect('party_list')
            except IntegrityError:
                context['message'] = "can't add person again"
        return super(TemplateView, self).render_to_response(context)


class ParticipantEditView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'

    def post(self, request, **kwargs):
        participant = Participant.objects.get(party=self.kwargs.get('pk'), user=request.user)
        if 'join' in request.POST:
            participant.status = Participant.JOINED
            participant.save()
        else:
            participant.status = Participant.LEFT
            participant.save()
        return redirect('party_list')

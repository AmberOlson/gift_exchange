
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


class SignUpInvitedView(TemplateView):
    login_url = '/login/'
    template_name = "signup_invited.html"

    def get_context_data(self, **kwargs):
        form = SignUpForm(self.request.POST or None)
        participant = Participant.objects.get(id=self.kwargs["pk"])
        context = {'form': form, 'participant': participant}
        return context

    def post(self, request, **kwargs):
        context = self.get_context_data()
        if context["form"].is_valid():
            username = context['form'].cleaned_data['username']
            email = context['form'].cleaned_data['email']
            password = context['form'].cleaned_data['password1']
            user = signup(username, email, password)

            if user is not None:
                participant = Participant.objects.get(id=self.kwargs["pk"])
                match_user_to_party(participant, user)
                login(request, user)
            return redirect('party_list')
        return super(TemplateView, self).render_to_response(context)


class SignUpView(TemplateView):
    login_url = '/login/'
    template_name = "signup.html"

    def get_context_data(self):
        form = SignUpForm(self.request.POST or None)
        context = {'form': form}
        return context

    def post(self, request):
        context = self.get_context_data()
        if context["form"].is_valid():
            username = context['form'].cleaned_data['username']
            email = context['form'].cleaned_data['email']
            password = context['form'].cleaned_data['password1']
            user = signup(username, email, password)

            if user is not None:
                login(request, user)
            return redirect('party_list')
        return super(TemplateView, self).render_to_response(context)


class LogOutView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'

    def logout_view(self, request):
        logout(request)
        return redirect('signup')

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from exchange.forms import PartyCreateForm
from exchange.models import Party
from django.contrib.auth.mixins import LoginRequiredMixin# Create your views here.

class PartyListView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "parties.html"


    def get_context_data(self):
        context = {'cat': 'candy', 'parties': Party.objects.all()}
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

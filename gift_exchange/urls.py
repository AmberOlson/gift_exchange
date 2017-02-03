"""gift_exchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from exchange.views.exchanges import ExchangeView
from exchange.views.signup import SignUpView, SignUpInvitedView, LogOutView
from exchange.views.particapant import ParticipantCreateView, ParticipantEditView
from exchange.views.party import PartyListView, PartyCreateView, PartyView, PartyDelete


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),
    url(r'^signup/$', SignUpView.as_view(), name="signup"),
    url(r'^signup/invited/(?P<pk>[0-9]+)$', SignUpInvitedView.as_view(), name="signup_invited"),
    url(r'^logout/$', LogOutView.as_view(), name="logout"),
    url(r'^parties/$', PartyListView.as_view(), name="party_list"),
    url(r'^party/$', PartyCreateView.as_view(), name="party_create"),
    url(r'^party/(?P<pk>[0-9]+)/view/$', PartyView.as_view(), name='party_view'),
    url(r'^party/(?P<pk>[0-9]+)/delete/$', PartyDelete.as_view(), name='party_delete'),
    url(r'^party/(?P<pk>[0-9]+)/guests/$', ParticipantCreateView.as_view(), name="party_participant_create"),
    url(r'^party/(?P<pk>[0-9]+)/guests/edit$', ParticipantEditView.as_view(), name="party_participant_edit"),
    url(r'^party/(?P<pk>[0-9]+)/exchange/$', ExchangeView.as_view(), name="party_exchange"),
]

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
from exchange.views import PartyListView, PartyCreateView, PartyView, ParticipantCreateView, ExchangeView, SignUpView, PartyDelete, ParticipantEditView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),
    url(r'^signup/$', SignUpView.as_view(), name="signup"),
    url(r'^parties/$', PartyListView.as_view(), name="party_list"),
    url(r'^party/$', PartyCreateView.as_view(), name="party_create"),
    url(r'^party/(?P<pk>[0-9]+)/view/$', PartyView.as_view(), name='party_view'),
    url(r'^party/(?P<pk>[0-9]+)/delete/$', PartyDelete.as_view(), name='party_delete'),
    url(r'^party/(?P<pk>[0-9]+)/guests/$', ParticipantCreateView.as_view(), name="party_participant_create"),
    url(r'^party/(?P<pk>[0-9]+)/guests/edit$', ParticipantEditView.as_view(), name="party_participant_edit"),
    url(r'^party/(?P<pk>[0-9]+)/exchange/$', ExchangeView.as_view(), name="party_exchange"),
]

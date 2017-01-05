from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse
from exchange.models import Party, Exchange, Participant
from exchange.domain import start_exchange


class ExchangeTestCase(TestCase):
    def test_start_exchange(self):
        """
        set up a party,
        add participanets
        start the Exchange
        assert echange were correclty created
        """
        party = Party.objects.create()
        participant1 = Participant.objects.create(party=party)
        participant2 = Participant.objects.create(party=party)
        started_party, _ = start_exchange(party)
        self.assertEqual(started_party.status, "started")
        self.assertEqual(1, Exchange.objects.filter(giver=participant1, party=party).count())
        self.assertEqual(1, Exchange.objects.filter(receiver=participant1, party=party).count())
        self.assertEqual(1, Exchange.objects.filter(giver=participant2, party=party).count())
        self.assertEqual(1, Exchange.objects.filter(receiver=participant2, party=party).count())


class CreatePartyTestCase(TestCase):

    def test_create_party(self):
        User.objects.create_user(username="alex", email="alex@example.com", password="password")
        self.client.login(username="alex", password="password")

        form_data = {"name": "My Fun Party"}
        response = self.client.post(reverse('party_create'), form_data)

        self.assertEqual(302, response.status_code)
        self.assertEquals(reverse('party_list'), response.url)
        self.assertTrue(Party.objects.get(name="My Fun Party"))

    def test_create_party__login_required__user_not_logged_in(self):
        form_data = {"name": "My Fun Party"}
        response = self.client.post(reverse('party_create'), form_data)

        self.assertEqual(302, response.status_code)
        self.assertEquals("%s?next=%s" % (reverse('login'), reverse('party_create')), response.url)
        self.assertFalse(Party.objects.all().exists())

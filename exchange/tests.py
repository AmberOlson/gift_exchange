from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse
from exchange.models import Party, Exchange, Participant
from exchange.domain import start_exchange
from django.core import mail


class GiftExchangeTestCase(TestCase):

    def create_and_login_user(self):
        self.admin_user = User.objects.create_user(username="alex2", email="alex2@example.com", password="password")
        self.client.login(username="alex2", password="password")


class ExchangeTestCase(GiftExchangeTestCase):

    def setUp(self):
        self.create_and_login_user()

    def test_start_exchange(self):
        """
        set up a party,
        add participanets
        start the Exchange
        assert echange were correclty created
        """
        # self.create_and_login_user()
        party = Party.objects.create()
        participant1 = Participant.objects.create(party=party)
        participant2 = Participant.objects.create(party=party)
        started_party, _ = start_exchange(party)
        self.assertEqual(started_party.status, "started")
        self.assertEqual(1, Exchange.objects.filter(giver=participant1, party=party).count())
        self.assertEqual(1, Exchange.objects.filter(receiver=participant1, party=party).count())
        self.assertEqual(1, Exchange.objects.filter(giver=participant2, party=party).count())
        self.assertEqual(1, Exchange.objects.filter(receiver=participant2, party=party).count())


class CreatePartyTestCase(GiftExchangeTestCase):

    def test_create_party(self):
        # User.objects.create_user(username="alex", email="alex@example.com", password="password")
        # self.client.login(username="alex", password="password")
        self.create_and_login_user()

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

class CreateParticipant(GiftExchangeTestCase):

    def setUp(self):
        # self.admin_user = User.objects.create_user(username="alex2", email="alex2@example.com", password="password")
        # self.client.login(username="alex2", password="password")
        self.create_and_login_user()

        self.invited_user = User.objects.create_user(username="amber", email="amber@example.com", password="password")
        self.party = Party.objects.create()

    def test_add_participant(self):
        form_data = {"participant": self.invited_user.email}
        response = self.client.post(reverse('party_participant_create', kwargs={'pk': self.party.id}), form_data)
        self.assertEqual(302, response.status_code)
        self.assertEquals(reverse('party_list'), response.url)
        self.assertTrue(Participant.objects.get(user=self.invited_user.id, party=self.party.id, admin="False"))

    def test_add_a_non_user(self):
        form_data = {"participant": "notuser@example.com"}
        response = self.client.post(reverse('party_participant_create', kwargs={'pk': self.party.id}), form_data)
        self.assertEqual(302, response.status_code)
        self.assertEqual(len(mail.outbox), 1)
        #somehow confirm that the user id is null?
        self.assertTrue(Participant.objects.get(party=self.party.id, admin="False"))
        self.assertEqual(mail.outbox[0].subject, 'HI')
        self.assertEqual(mail.outbox[0].to, ["notuser@example.com"])
        self.assertIn('www.localhost//signup/invited/1', mail.outbox[0].body)
        # a line in the shows what link is sent in the email
        self.assertEquals(reverse('party_list'), response.url)
        self.client.logout()
        participant = Participant.objects.last()
        form_data = {"username": "Candy", "email": "candy@example.com", "password": "password"}
        response = self.client.post(reverse('signup_invited', kwargs={'pk': participant.id}), form_data)
        self.assertEqual(302, response.status_code)
        user = User.objects.get(username= "Candy")
        self.assertTrue(Participant.objects.get(user=user.id, party=self.party.id, admin=False))

class signup(GiftExchangeTestCase):

    def test_sign_up(self):
        form_data = {"username": "Amber", "email": "amberolson@gmail.com", "password": "password"}
        response = self.client.post(reverse('signup'), form_data)

        self.assertEqual(302, response.status_code)
        self.assertEquals(reverse('party_list'), response.url)
        self.assertTrue(User.objects.get(username="Amber", email="amberolson@gmail.com"))

from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse
from exchange.models import Party, Exchange, Participant
from exchange.domain import start_exchange
from django.core import mail
from django.db import IntegrityError
from exchange.factories import create_party, create_user, create_participant


class GiftExchangeTestCase(TestCase):

    def create_and_login_user(self):
        self.admin_user = User.objects.create_user(username="alex2", email="alex2@example.com", password="password")
        self.client.login(username="alex2", password="password")


class ExchangeTestCase(GiftExchangeTestCase):

    def setUp(self):
        self.create_and_login_user()
        self.party = Party.objects.create()
        # self.participant1 = Participant.objects.create(party=self.party, status=Participant.JOINED)
        self.participant1 = create_participant(party=self.party, status=Participant.JOINED)
        self.participant2 = Participant.objects.create(party=self.party, status=Participant.JOINED)

    def test_start_exchange(self):

        started_party, _ = start_exchange(self.party)
        self.assertEqual(started_party.status, Party.STARTED)
        self.assertEqual(1, Exchange.objects.filter(giver=self.participant1, party=self.party).count())
        self.assertEqual(1, Exchange.objects.filter(receiver=self.participant1, party=self.party).count())
        self.assertEqual(1, Exchange.objects.filter(giver=self.participant2, party=self.party).count())
        self.assertEqual(1, Exchange.objects.filter(receiver=self.participant2, party=self.party).count())

    def test_no_participating_exchange(self):
        participant3 = Participant.objects.create(party=self.party, status=Participant.LEFT)
        participant4 = Participant.objects.create(party=self.party, status=Participant.INVITED)

        started_party, _ = start_exchange(self.party)
        self.assertEqual(started_party.status, Party.STARTED)
        self.assertEqual(1, Exchange.objects.filter(giver=self.participant1, party=self.party).count())
        self.assertEqual(1, Exchange.objects.filter(receiver=self.participant1, party=self.party).count())
        self.assertEqual(1, Exchange.objects.filter(giver=self.participant2, party=self.party).count())
        self.assertEqual(1, Exchange.objects.filter(receiver=self.participant2, party=self.party).count())

        self.assertEqual(0, Exchange.objects.filter(giver=participant3, party=self.party).count())
        self.assertEqual(0, Exchange.objects.filter(receiver=participant3, party=self.party).count())

        self.assertEqual(0, Exchange.objects.filter(giver=participant4, party=self.party).count())
        self.assertEqual(0, Exchange.objects.filter(receiver=participant4, party=self.party).count())

    def test_second_exchange_attempt(self):
        start_exchange(self.party)
        with self.assertRaises(Exception) as context:
            start_exchange(self.party)

        self.assertTrue('exchanges already created' in context.exception)


class CreatePartyTestCase(GiftExchangeTestCase):

    def test_create_party(self):
        self.create_and_login_user()

        form_data = {"name": "My Fun Party"}
        response = self.client.post(reverse('party_create'), form_data)

        self.assertEqual(302, response.status_code)
        self.assertEquals(reverse('party_list'), response.url)
        self.assertTrue(Party.objects.get(name="My Fun Party"))
        self.assertTrue(Participant.objects.get(user=self.admin_user, admin=True))

    def test_create_party_invalid_form(self):
        self.create_and_login_user()

        form_data = {"name": ""}
        response = self.client.post(reverse('party_create'), form_data)
        self.assertContains(response, 'This field is required.', 1, 200)

    def test_create_party__login_required__user_not_logged_in(self):
        form_data = {"name": "My Fun Party"}
        response = self.client.post(reverse('party_create'), form_data)

        self.assertEqual(302, response.status_code)
        self.assertEquals("%s?next=%s" % (reverse('login'), reverse('party_create')), response.url)
        self.assertFalse(Party.objects.all().exists())


class EditPartyTestCase(GiftExchangeTestCase):
    def setUp(self):
        self.create_and_login_user()
        self.party = Party.objects.create(name="My Fun Party")
        Participant.objects.create(user=self.admin_user, party=self.party)

    def test_edit_party(self):
        form_data = {"name": "New Party Name"}
        response = self.client.post(reverse('party_view', kwargs={'pk': self.party.id}), form_data)

        self.assertEqual(302, response.status_code)
        self.assertEquals(reverse('party_list'), response.url)
        self.assertTrue(Party.objects.get(name="New Party Name"))
        self.assertFalse(Party.objects.filter(name="My Fun Party"))

    def test_delete(self):
        response = self.client.post(reverse('party_delete', kwargs={'pk': self.party.id}))
        self.assertEqual(302, response.status_code)
        self.assertEquals(reverse('party_list'), response.url)
        self.assertFalse(Party.objects.filter(name="My Fun Party"))


class CreateParticipant(GiftExchangeTestCase):

    def setUp(self):
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
        self.assertTrue(Participant.objects.get(party=self.party.id, admin="False", user=None))
        self.assertEqual(mail.outbox[0].subject, 'HI')
        self.assertEqual(mail.outbox[0].to, ["notuser@example.com"])
        self.assertIn('localhost:8000/signup/invited/1', mail.outbox[0].body)
        self.assertEquals(reverse('party_list'), response.url)
        self.client.logout()
        participant = Participant.objects.last()

        form_data = {"username": "Candy", "email": "candy@example.com", "password1": "password", "password2": "password"}
        response = self.client.post(reverse('signup_invited', kwargs={'pk': participant.id}), form_data)
        self.assertEqual(302, response.status_code)
        user = User.objects.get(username="Candy")
        self.assertTrue(Participant.objects.get(user=user.id, party=self.party.id, admin=False))

    def test_add_same_user(self):
        Participant.objects.create(user=self.invited_user, party=self.party)
        with self.assertRaises(IntegrityError):
            Participant.objects.create(user=self.invited_user, party=self.party)

    def test_create_participant_empty_form(self):
        form_data = {"participant": ""}
        response = self.client.post(reverse('party_participant_create', kwargs={'pk': self.party.id}), form_data)
        self.assertContains(response, 'This field is required.', 1, 200)

    def test_create_participant_not_email_form(self):
        form_data = {"participant": "amber"}
        response = self.client.post(reverse('party_participant_create', kwargs={'pk': self.party.id}), form_data)
        self.assertContains(response, 'Enter a valid email address', 1, 200)


class ParticipantAccepting(GiftExchangeTestCase):

    def setUp(self):
        self.create_and_login_user()

    def test_accepting_invite(self):
        self.invited_user = User.objects.create_user(username="amber", email="amber@example.com", password="password")
        self.party = Party.objects.create()
        self.participant = Participant.objects.create(party=self.party, user=self.admin_user)
        response = self.client.post(reverse('party_participant_edit', kwargs={'pk': self.party.id}), {'join': [u'Join Exchange']})
        self.assertEqual(302, response.status_code)
        self.assertEquals(reverse('party_list'), response.url)
        self.assertTrue(Participant.objects.get(user=self.admin_user, party=self.party, admin="False", status=Participant.JOINED))

    def test_not_accepting_invite(self):
        self.invited_user = User.objects.create_user(username="amber", email="amber@example.com", password="password")
        self.party = Party.objects.create()
        self.participant = Participant.objects.create(party=self.party, user=self.admin_user)
        response = self.client.post(reverse('party_participant_edit', kwargs={'pk': self.party.id}), {'left': [u'Leave Exchange']})
        self.assertEqual(302, response.status_code)
        self.assertEquals(reverse('party_list'), response.url)
        self.assertTrue(Participant.objects.get(user=self.admin_user, party=self.party, admin="False", status=Participant.LEFT))


class signup(GiftExchangeTestCase):

    def test_sign_up(self):
        form_data = {"username": "Amber", "email": "amberolson@gmail.com", "password1": "password", "password2": "password"}
        response = self.client.post(reverse('signup'), form_data)

        self.assertEqual(302, response.status_code)
        self.assertEquals(reverse('party_list'), response.url)
        self.assertTrue(User.objects.get(username="Amber", email="amberolson@gmail.com"))

from django.test import TestCase
from exchange.models import Party, Exchange, Participant
from exchange.domain import start_exchange

# Create your tests here.
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

from exchange.models import Party, Participant
from django.contrib.auth.models import User


def create_party(title='Party'):
    party = Party.objects.create(name=title)
    return party


def create_user(name='Corbin', email='corbin@example.com', password='password'):
    user = User.objects.create(name=name, email=email, password=password)
    return user


def create_participant(party, user=None, admin=False, status=Participant.INVITED):
    participant = Participant.objects.create(party=party, user=user, admin=admin, status=status)
    return participant

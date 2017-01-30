from django.contrib.auth import authenticate, login
from exchange.models import Participant
from django.contrib.auth.models import User


def signup(username, email, password):
    User.objects.create_user(username=username, email=email, password=password)
    username = username
    password = password
    user = authenticate(username=username, password=password)
    return user


def match_user_to_party(participant, user):
    participant.user_id = user.id
    participant.save()

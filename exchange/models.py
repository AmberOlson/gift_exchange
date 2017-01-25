from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Party(models.Model):
    JOINING = 'joining'
    STARTED = 'started'

    STATUS_CHOICES = (
        ("JOINING", 'joining'),
        ("STARTED", 'started')
    )
    status = models.CharField(default='JOINING', max_length=255, choices=STATUS_CHOICES)
    name = models.CharField(max_length=255)


class Participant(models.Model):
    JOINED = "joined"
    LEFT = 'left'
    INVITED = 'invited'

    STATUS_CHOICES =(
        ('JOINED', 'joined'),
        ('INVITED', 'invited'),
        ('LEFT', 'left'),
    )

    party = models.ForeignKey(Party)
    admin = models.BooleanField(default=False)
    user = models.ForeignKey(User, blank=True, null=True)
    status = models.CharField(default='INVITED', max_length=255, choices=STATUS_CHOICES)

    class Meta:
        unique_together = (("party", "user"),)


class Exchange(models.Model):
    party = models.ForeignKey(Party)
    giver = models.ForeignKey(Participant, related_name="giver")
    receiver = models.ForeignKey(Participant, related_name="receiver")

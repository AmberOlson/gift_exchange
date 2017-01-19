from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Party(models.Model):
    status = models.CharField(default='joining', max_length=255)
    name = models.CharField(max_length=255)

class Participant(models.Model):
    party = models.ForeignKey(Party)
    admin = models.BooleanField(default=False)
    user = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        unique_together = (("party", "user"),)

class Exchange(models.Model):
    party = models.ForeignKey(Party)
    giver = models.ForeignKey(Participant, related_name="giver")
    receiver = models.ForeignKey(Participant, related_name="receiver")

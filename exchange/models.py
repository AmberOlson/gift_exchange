from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Party(models.Model):
    status = models.CharField(default='joining', max_length=255)
    name = models.CharField(max_length=255)

class Participant(models.Model):
    party = models.ForeignKey(Party)

class Exchange(models.Model):
    party = models.ForeignKey(Party)
    giver = models.ForeignKey(Participant, related_name="giver")
    receiver = models.ForeignKey(Participant, related_name="receiver")

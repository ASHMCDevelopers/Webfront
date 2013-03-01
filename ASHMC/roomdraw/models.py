from django.db import models
from django.contrib.auth.models import User

from ASHMC.roster.models import DormRoom
# Create your models here.

class RoomInterest(models.Model):
    room = models.ForeignKey(DormRoom)
    users = models.ManyToManyField(User)

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from platformerdemonlist.models.platformerlevel import PlatformerLevel

# Create your models here.

class PlatformerListChange(models.Model):
    pass
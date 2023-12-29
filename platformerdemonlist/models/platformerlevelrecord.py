from django.db import models
from platformerdemonlist.models.platformerplayer import PlatformerPlayer
from platformerdemonlist.models.platformerlevel import PlatformerLevel
import math
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class PlatformerLevelRecord(models.Model):
    pass
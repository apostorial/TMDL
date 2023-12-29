from django.db import models
import math
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class PlatformerLevel(models.Model):
    pass
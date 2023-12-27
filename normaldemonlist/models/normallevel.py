from django.db import models
import math
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class NormalLevel(models.Model):
    DIFFICULTIES = [
        ('Hard Demon', 'Hard Demon'),
        ('Insane Demon', 'Insane Demon'),
        ('Extreme Demon', 'Extreme Demon'),
    ]

    DURATIONS = [
        ('Tiny', 'Tiny'),
        ('Short', 'Short'),
        ('Medium', 'Medium'),
        ('Long', 'Long'),
        ('XL', 'XL'),
    ]

    levelid = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    ranking = models.PositiveIntegerField(default=0)
    difficulty = models.CharField(max_length=255, choices=DIFFICULTIES, blank=True)
    duration = models.CharField(max_length=255, choices=DURATIONS, blank=True)
    youtube_link = models.URLField(blank=True)
    youtube_thumbnail = models.URLField(blank=True)
    points = models.FloatField(default=0)
    min_points = models.FloatField(default=0)
    min_completion = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    first_victor = models.ForeignKey('normaldemonlist.NormalPlayer', on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.ranking is not None:
            self.points = round(500 * (1 - math.log(self.ranking, 151)), 2)
            self.min_points = round((500 * (1 - math.log(self.ranking, 151))) * 1/3, 2)
        else:
            self.points = None
            self.min_points = None

        super(NormalLevel, self).save(*args, **kwargs)
  
    def __str__(self):
        return f"{self.levelid} - {self.name}"
    
@receiver(post_save, sender='normaldemonlist.NormalPlayer')
@receiver(post_save, sender='normaldemonlist.NormalLevelRecord')
def update_region_points(sender, instance, **kwargs):
    from normaldemonlist.models.normalplayer import NormalPlayer
    from normaldemonlist.models.normallevelrecord import NormalLevelRecord
    
    if isinstance(instance, NormalPlayer):
        region = instance.region
    elif isinstance(instance, NormalLevelRecord):
        region = instance.player.region
    
    region.points = region.calculate_points()
    region.save()

@receiver(post_save, sender=NormalLevel)
def create_level_record(sender, instance, created, **kwargs):
    from normaldemonlist.models.normallevelrecord import NormalLevelRecord
    if created and instance.first_victor:
        player = instance.first_victor
        level_record = NormalLevelRecord.objects.create(player=player, level=instance, record_percentage=100)

@receiver(post_save, sender=NormalLevel)
def update_min_completion(sender, instance, **kwargs):
    if instance.ranking > 75 and instance.min_completion != 100:
        instance.min_completion = 100
        instance.save(update_fields=['min_completion'])
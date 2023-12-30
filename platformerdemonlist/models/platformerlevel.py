from django.db import models
import math
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class PlatformerLevel(models.Model):
    DIFFICULTIES = [
        ('Hard Demon', 'Hard Demon'),
        ('Insane Demon', 'Insane Demon'),
        ('Extreme Demon', 'Extreme Demon'),
    ]

    levelid = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    ranking = models.PositiveIntegerField(default=0)
    difficulty = models.CharField(max_length=255, choices=DIFFICULTIES, blank=True)
    youtube_link = models.URLField(blank=True)
    youtube_thumbnail = models.URLField(blank=True)
    points = models.FloatField(default=0)
    record_holder = models.ForeignKey('platformerdemonlist.PlatformerPlayer', on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.ranking is not None:
            self.points = round(500 * (1 - math.log(self.ranking, 151)), 2)
        else:
            self.points = None

        super(PlatformerLevel, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name', 'points']
        verbose_name = "Platformer Level"
        verbose_name_plural = "Platformer Levels"
  
    def __str__(self):
        return f"{self.levelid} - {self.name}"
    
@receiver(post_save, sender='platformerdemonlist.PlatformerPlayer')
@receiver(post_save, sender='platformerdemonlist.PlatformerLevelRecord')
def update_region_points(sender, instance, **kwargs):
    from platformerdemonlist.models.platformerplayer import PlatformerPlayer
    from platformerdemonlist.models.platformerlevelrecord import PlatformerLevelRecord
    
    if isinstance(instance, PlatformerPlayer):
        region = instance.region
    elif isinstance(instance, PlatformerLevelRecord):
        region = instance.player.region
    
    region.points = region.calculate_points()
    region.save()

@receiver(post_save, sender=PlatformerLevel)
def create_level_record(sender, instance, created, **kwargs):
    from platformerdemonlist.models.platformerlevelrecord import PlatformerLevelRecord
    if created and instance.record_holder:
        player = instance.record_holder
        level_record = PlatformerLevelRecord.objects.create(player=player, level=instance)
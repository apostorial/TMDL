from django.db import models
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

class PlatformerPlayer(models.Model):
    name = models.CharField(max_length=255)
    points = models.FloatField(default=0)
    region = models.ForeignKey('platformerdemonlist.PlatformerRegion', on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.name} - {round(self.points, 2)} points"
    
@receiver(post_save, sender='platformerdemonlist.PlatformerPlayer')
@receiver(post_save, sender='platformerdemonlist.PlatformerLevelRecord')
def update_player_points(sender, instance, **kwargs):
    player_model = apps.get_model('platformerdemonlist', 'PlatformerPlayer')
    level_record_model = apps.get_model('platformerdemonlist', 'PlatformerLevelRecord')
    
    if sender == player_model:
        player = instance
    elif sender == level_record_model:
        player = instance.player
    
    total_points = 0

    for level_record in player.platformerlevelrecord_set.all():
        level = level_record.level
        total_points += level.points

    if player.points != total_points:
        player.points = total_points
        player.save(update_fields=['points'])

@receiver(post_save, sender='platformerdemonlist.PlatformerPlayer')
@receiver(post_save, sender='platformerdemonlist.PlatformerLevelRecord')
def update_region_points(sender, instance, **kwargs):
    if sender == 'platformerdemonlist.PlatformerPlayer':
        from platformerdemonlist.models.platformerplayer import PlatformerPlayer
        region = instance.region
        region.points = region.calculate_points()
        region.save()
    elif sender == 'platformerdemonlist.PlatformerRecord':
        from platformerdemonlist.models.platformerplayer import PlatformerPlayer
        player = instance.player
        region = player.region
        region.points = region.calculate_points()
        region.save()
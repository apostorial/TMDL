from django.db import models
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

class NormalPlayer(models.Model):
    name = models.CharField(max_length=255)
    points = models.FloatField(default=0)
    region = models.ForeignKey('normaldemonlist.NormalRegion', on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.name} - {round(self.points, 2)} points"
    
@receiver(post_save, sender='normaldemonlist.NormalPlayer')
@receiver(post_save, sender='normaldemonlist.NormalLevelRecord')
def update_player_points(sender, instance, **kwargs):
    player_model = apps.get_model('normaldemonlist', 'NormalPlayer')
    level_record_model = apps.get_model('normaldemonlist', 'NormalLevelRecord')
    
    if sender == player_model:
        player = instance
    elif sender == level_record_model:
        player = instance.player
    
    total_points = 0

    for level_record in player.normallevelrecord_set.all():
        level = level_record.level
        record_percentage = level_record.record_percentage

        if record_percentage == 100:
            total_points += level.points
        else:
            total_points += level.points * 1/3

    if player.points != total_points:
        player.points = total_points
        player.save(update_fields=['points'])

@receiver(post_save, sender='normaldemonlist.NormalPlayer')
@receiver(post_save, sender='normaldemonlist.NormalLevelRecord')
def update_region_points(sender, instance, **kwargs):
    if sender == 'normaldemonlist.NormalPlayer':
        from normaldemonlist.models.normalplayer import NormalPlayer
        region = instance.region
        region.points = region.calculate_points()
        region.save()
    elif sender == 'normaldemonlist.LevelRecord':
        from normaldemonlist.models.normalplayer import NormalPlayer
        player = instance.player
        region = player.region
        region.points = region.calculate_points()
        region.save()
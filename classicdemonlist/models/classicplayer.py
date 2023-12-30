from django.db import models
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

class ClassicPlayer(models.Model):
    name = models.CharField(max_length=255)
    points = models.FloatField(default=0)
    region = models.ForeignKey('classicdemonlist.ClassicRegion', on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.name} - {round(self.points, 2)} points"
    
@receiver(post_save, sender='classicdemonlist.ClassicPlayer')
@receiver(post_save, sender='classicdemonlist.ClassicLevelRecord')
def update_player_points(sender, instance, **kwargs):
    player_model = apps.get_model('classicdemonlist', 'ClassicPlayer')
    level_record_model = apps.get_model('classicdemonlist', 'ClassicLevelRecord')
    
    if sender == player_model:
        player = instance
    elif sender == level_record_model:
        player = instance.player
    
    total_points = 0

    for level_record in player.classiclevelrecord_set.all():
        level = level_record.level
        record_percentage = level_record.record_percentage

        if record_percentage == 100:
            total_points += level.points
        else:
            total_points += level.points * 1/3

    if player.points != total_points:
        player.points = total_points
        player.save(update_fields=['points'])

@receiver(post_save, sender='classicdemonlist.ClassicPlayer')
@receiver(post_save, sender='classicdemonlist.ClassicLevelRecord')
def update_region_points(sender, instance, **kwargs):
    if sender == 'classicdemonlist.ClassicPlayer':
        from classicdemonlist.models.classicplayer import ClassicPlayer
        region = instance.region
        region.points = region.calculate_points()
        region.save()
    elif sender == 'classicdemonlist.ClassicLevelRecord':
        from classicdemonlist.models.classicplayer import ClassicPlayer
        player = instance.player
        region = player.region
        region.points = region.calculate_points()
        region.save()
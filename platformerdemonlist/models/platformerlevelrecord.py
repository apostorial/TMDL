from django.db import models
from platformerdemonlist.models.platformerplayer import PlatformerPlayer
from platformerdemonlist.models.platformerlevel import PlatformerLevel
import math
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

class PlatformerLevelRecord(models.Model):
    player = models.ForeignKey(PlatformerPlayer, on_delete=models.CASCADE)
    level = models.ForeignKey(PlatformerLevel, on_delete=models.CASCADE, null=True)
    record_time = models.DurationField(default=timedelta(minutes=30))
    record_video_link = models.URLField(blank=True)

    class Meta:
        unique_together = ['level', 'player']

    def update_player_points(self):
        level = self.level
        player = self.player
        points = level.points

        if player.points != points:
            player.points = points
            player.save(update_fields=['points'])

    def save(self, *args, **kwargs):
        if self.pk is None:
            if not self.level.record_holder:
                self.level.record_holder = self.player
                self.level.save()

        super(PlatformerLevelRecord, self).save(*args, **kwargs)
        self.update_player_points()

    def __str__(self):
        return f"{self.player.name} - {self.level.name} ({self.record_time})"
    
@receiver(post_save, sender=PlatformerLevelRecord)
def update_player_points_signal(sender, instance, **kwargs):
    instance.update_player_points()
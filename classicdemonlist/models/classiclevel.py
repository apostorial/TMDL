from django.db import models
import math
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class ClassicLevel(models.Model):
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
    first_victor = models.ForeignKey('classicdemonlist.ClassicPlayer', on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.ranking is not None:
            self.points = round(500 * (1 - math.log(self.ranking, 151)), 2)
            self.min_points = round((500 * (1 - math.log(self.ranking, 151))) * 1/3, 2)
        else:
            self.points = None
            self.min_points = None

        super(ClassicLevel, self).save(*args, **kwargs)
  
    def __str__(self):
        return f"{self.levelid} - {self.name}"
    
@receiver(post_save, sender='classicdemonlist.ClassicPlayer')
@receiver(post_save, sender='classicdemonlist.ClassicLevelRecord')
def update_region_points(sender, instance, **kwargs):
    from classicdemonlist.models.classicplayer import ClassicPlayer
    from classicdemonlist.models.classiclevelrecord import ClassicLevelRecord
    
    if isinstance(instance, ClassicPlayer):
        region = instance.region
    elif isinstance(instance, ClassicLevelRecord):
        region = instance.player.region
    
    region.points = region.calculate_points()
    region.save()

@receiver(post_save, sender=ClassicLevel)
def create_level_record(sender, instance, created, **kwargs):
    from classicdemonlist.models.classiclevelrecord import ClassicLevelRecord
    if created and instance.first_victor:
        player = instance.first_victor
        if instance.youtube_link:
            record_video_link = instance.youtube_link
            level_record = ClassicLevelRecord.objects.create(player=player, level=instance, record_percentage=100, record_video_link=record_video_link)
        else:
            print(instance.youtube_link)
            level_record = ClassicLevelRecord.objects.create(player=player, level=instance, record_percentage=100)

@receiver(post_save, sender=ClassicLevel)
def update_min_completion(sender, instance, **kwargs):
    if instance.ranking > 75 and instance.min_completion != 100:
        instance.min_completion = 100
        instance.save(update_fields=['min_completion'])
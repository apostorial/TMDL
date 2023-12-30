from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from platformerdemonlist.models.platformerlevel import PlatformerLevel

# Create your models here.

class PlatformerListChange(models.Model):

    place = 'Place'
    #move = 'Move'
    raise_ = 'Raise'
    lower = 'Lower'
    swap = 'Swap'
    remove = 'Remove'
    list_requirement = 'List requirement'

    CHANGE_TYPE = [
        ('Place', 'Place'),
        #('Move', 'Move'),
        ('Raise', 'Raise'),
        ('Lower', 'Lower'),
        ('Swap', 'Swap'),
        ('Remove', 'Remove'),
        ('List requirement', 'List requirement'),
    ]

    level = models.ForeignKey(PlatformerLevel, on_delete=models.SET_NULL, blank=True, null=True)
    swap_with = models.ForeignKey(PlatformerLevel, related_name='swap_with', on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField()
    change_type = models.CharField(max_length=255, choices=CHANGE_TYPE, default=None)
    placement = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=255, blank=True)
    above_level = models.ForeignKey(PlatformerLevel, related_name='above_level', on_delete=models.SET_NULL, blank=True, null=True)
    below_level = models.ForeignKey(PlatformerLevel, related_name='below_level', on_delete=models.SET_NULL, blank=True, null=True)
    effect = models.CharField(max_length=255, blank=True)

    custom_levelname = models.CharField(max_length=100, blank=True, null=True)
    custom_swapwith = models.CharField(max_length=100, blank=True, null=True)
    custom_abovelevelname = models.CharField(max_length=100, blank=True, null=True)
    custom_belowlevelname = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Platformer List Change"
        verbose_name_plural = "Platformer List Changes"

@receiver(pre_save, sender=PlatformerListChange)
def populate_description(sender, instance, **kwargs):
    if instance.level:
        level_name = instance.level.name
    elif instance.custom_levelname:
        level_name = instance.custom_levelname
    if instance.above_level:
        abovelevel_name = instance.above_level.name
    elif instance.custom_abovelevelname:
        abovelevel_name = instance.custom_abovelevelname
    if instance.below_level:
        belowlevel_name = instance.below_level.name
    elif instance.custom_belowlevelname:
        belowlevel_name = instance.custom_belowlevelname
    if instance.swap_with:
        swapwith_name = instance.swap_with.name
    elif instance.custom_swapwith:
        swapwith_name = instance.customswapwith

    if instance.change_type == PlatformerListChange.place:
        instance.description = f"{level_name} has been placed at #{instance.placement}"
    #elif instance.change_type == ListChange.move:
        #instance.description = f"{level_name} has been moved to #{instance.placement}"
    elif instance.change_type == PlatformerListChange.swap:
        instance.description = f"{level_name} has been swapped with #{swapwith_name} at #{instance.placement}"
    elif instance.change_type == PlatformerListChange.raise_:
        instance.description = f"{level_name} has been raised to #{instance.placement}"
    elif instance.change_type == PlatformerListChange.lower:
        instance.description = f"{level_name} has been lowered to #{instance.placement}"
    elif instance.change_type == PlatformerListChange.remove:
        instance.description = f"{level_name} has been removed"
    elif instance.change_type == PlatformerListChange.list_requirement:
        instance.description = f"{level_name}'s list requirement has been changed to #{instance.level.min_completion}"

    if instance.above_level is not None:
        instance.description += f", above {abovelevel_name}"
    if instance.below_level is not None and instance.above_level is not None:
        instance.description += f" and below {belowlevel_name}"
    if instance.below_level is not None and instance.above_level is None:
        instance.description += f", below {belowlevel_name}"

    instance.description += "."
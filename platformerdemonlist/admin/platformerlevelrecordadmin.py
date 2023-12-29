from django.contrib import admin
from platformerdemonlist.models.platformerlevelrecord import PlatformerLevelRecord

# Register your models here.

class PlatformerLevelRecordAdmin(admin.ModelAdmin):
    list_display = ['player', 'level']
    search_fields = ['player__name', 'level__name']

admin.site.register(PlatformerLevelRecord, PlatformerLevelRecordAdmin)
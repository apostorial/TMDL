from django.contrib import admin
from platformerdemonlist.models.platformerlevelrecord import PlatformerLevelRecord

# Register your models here.

class PlatformerLevelRecordAdmin(admin.ModelAdmin):
    pass

admin.site.register(PlatformerLevelRecord, PlatformerLevelRecordAdmin)
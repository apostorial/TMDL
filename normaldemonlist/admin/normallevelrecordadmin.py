from django.contrib import admin
from normaldemonlist.models.normallevelrecord import NormalLevelRecord

# Register your models here.

class NormalLevelRecordAdmin(admin.ModelAdmin):
    list_display = ['player', 'level', 'record_percentage']
    search_fields = ['player__name', 'level__name']

admin.site.register(NormalLevelRecord, NormalLevelRecordAdmin)
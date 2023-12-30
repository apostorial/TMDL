from django.contrib import admin
from classicdemonlist.models.classiclevelrecord import ClassicLevelRecord

# Register your models here.

class ClassicLevelRecordAdmin(admin.ModelAdmin):
    list_display = ['player', 'level', 'record_percentage']
    search_fields = ['player__name', 'level__name']

admin.site.register(ClassicLevelRecord, ClassicLevelRecordAdmin)
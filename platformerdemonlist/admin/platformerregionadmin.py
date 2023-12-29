from django.contrib import admin
from platformerdemonlist.models.platformerregion import PlatformerRegion

# Register your models here.

class PlatformerRegionAdmin(admin.ModelAdmin):
    pass

admin.site.register(PlatformerRegion, PlatformerRegionAdmin)
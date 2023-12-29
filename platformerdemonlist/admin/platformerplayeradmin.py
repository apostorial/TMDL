from django.contrib import admin
from platformerdemonlist.models.platformerplayer import PlatformerPlayer

# Register your models here.

class PlatformerPlayerAdmin(admin.ModelAdmin):
    pass

admin.site.register(PlatformerPlayer, PlatformerPlayerAdmin)
from django.contrib import admin
from platformerdemonlist.models.platformerlistchange import PlatformerListChange

# Register your models here.

class PlatformerListChangeAdmin(admin.ModelAdmin):
    pass

admin.site.register(PlatformerListChange, PlatformerListChangeAdmin)
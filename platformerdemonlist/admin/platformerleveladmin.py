from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from platformerdemonlist.models.platformerlevel import PlatformerLevel

# Register your models here.

class CustomSortableAdminMixin(SortableAdminMixin):
    pass

class PlatformerLevelAdmin(CustomSortableAdminMixin, admin.ModelAdmin):
    pass

admin.site.register(PlatformerLevel, PlatformerLevelAdmin)
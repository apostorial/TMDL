from django.contrib import admin
from platformerdemonlist.models.platformerlistchange import PlatformerListChange

# Register your models here.

class PlatformerListChangeAdmin(admin.ModelAdmin):
    list_display = ['date', 'level', 'description', 'effect']
    search_fields = ['date', 'level']

    def add_view(self, request, form_url='', extra_context=None):
            self.exclude = ['description']
            return super().add_view(request, form_url, extra_context)

admin.site.register(PlatformerListChange, PlatformerListChangeAdmin)
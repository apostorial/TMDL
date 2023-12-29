from django.contrib import admin
from normaldemonlist.models.normallistchange import NormalListChange

# Register your models here.

class NormalListChangeAdmin(admin.ModelAdmin):
    list_display = ['date', 'level', 'description', 'effect']
    search_fields = ['date', 'level']

    def add_view(self, request, form_url='', extra_context=None):
            self.exclude = ['description']
            return super().add_view(request, form_url, extra_context)

admin.site.register(NormalListChange, NormalListChangeAdmin)
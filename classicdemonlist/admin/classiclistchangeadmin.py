from django.contrib import admin
from classicdemonlist.models.classiclistchange import ClassicListChange

# Register your models here.

class ClassicListChangeAdmin(admin.ModelAdmin):
    list_display = ['date', 'level', 'description', 'effect']
    search_fields = ['date', 'level']

    def add_view(self, request, form_url='', extra_context=None):
            self.exclude = ['description']
            return super().add_view(request, form_url, extra_context)

admin.site.register(ClassicListChange, ClassicListChangeAdmin)
from django.contrib import admin
from normaldemonlist.models.normalplayer import NormalPlayer

# Register your models here.

class NormalPlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'rounded_points', 'region']
    search_fields = ['name', 'region__name']

    def rounded_points(self, obj):
        return round(obj.points, 2)
    rounded_points.short_description = 'Points (rounded)'

    def add_view(self, request, form_url='', extra_context=None):
            self.exclude = ['points']
            return super().add_view(request, form_url, extra_context)

admin.site.register(NormalPlayer, NormalPlayerAdmin)
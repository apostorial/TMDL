from django.contrib import admin
from normaldemonlist.models.normalregion import NormalRegion

# Register your models here.

class NormalRegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'rounded_points']
    search_fields = ['name']

    def rounded_points(self, obj):
        return round(obj.points, 2)
    rounded_points.short_description = 'Points (rounded)'

    def add_view(self, request, form_url='', extra_context=None):
            self.exclude = ['points']
            return super().add_view(request, form_url, extra_context)

admin.site.register(NormalRegion, NormalRegionAdmin)
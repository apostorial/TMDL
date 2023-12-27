from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from normaldemonlist.models.normallevel import NormalLevel
import math, gd, asyncio
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from pytube import YouTube

# Register your models here.

class CustomSortableAdminMixin(SortableAdminMixin):
    def _update_order(self, updated_items, extra_model_filters):
        super()._update_order(updated_items, extra_model_filters)
        for item in updated_items:
            level = NormalLevel.objects.get(pk=item[0])
            level.save()
            for level_record in level.normallevelrecord_set.all():
                level_record.save()

class NormalLevelAdmin(CustomSortableAdminMixin, admin.ModelAdmin):
    list_display = ['ranking', 'name', 'points', 'min_points', 'min_completion', 'first_victor']
    search_fields = ['name', 'levelid']
    ordering = ['ranking']
    actions = ['save_all']

    def save_model(self, request, obj, form, change):
        level_id = form.cleaned_data.get('levelid')
        youtube_link = form.cleaned_data.get('youtube_link')

        if level_id:
            try:
                level_data = asyncio.run(gd.Client().get_level(level_id))
                
                obj.name = level_data.name
                obj.publisher = level_data.creator.name
                if level_data.length.name != "XL":
                    obj.duration = level_data.length.name.capitalize()
                else:
                    obj.duration = level_data.length.name
                obj.difficulty = level_data.difficulty.name.replace('_', ' ').title()
                obj.youtube_thumbnail = YouTube(youtube_link).thumbnail_url
            
            except Exception as e:
                print(f"Error fetching level data: {e}")

        super().save_model(request, obj, form, change)

    def save_all(self, request, queryset):
        for obj in queryset:
            obj.points = round(500 * (1 - math.log(obj.ranking, 151)), 2)
            obj.min_points = round((500 * (1 - math.log(obj.ranking, 151))) * 1/3, 2)
            obj.save()

            for level_record in obj.levelrecord_set.all():
                level_record.save()

        self.message_user(request, f"{queryset.count()} levels saved successfully.")

    save_all.short_description = "Save selected levels"
    
    def add_view(self, request, form_url='', extra_context=None):
            self.exclude = ['points', 'min_points']
            return super().add_view(request, form_url, extra_context)

admin.site.register(NormalLevel, NormalLevelAdmin)
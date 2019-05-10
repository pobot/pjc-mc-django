from django.contrib import admin

from solo.admin import SingletonModelAdmin

from .models import *


@admin.register(DisplaySettings)
class DisplayAdmin(SingletonModelAdmin):
    actions = None
    list_display = ['summary', 'action']
    list_display_links = ['action']
    fieldsets = (
        ('Pagination', {
            'fields': ('delay',)
        }),
        ('Pages affichées', {
            'fields': DISPLAY_NAMES
        }),
        ('Diffusion message', {
            'fields': ('message',)
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return not DisplaySettings.objects.exists()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['delay'].widget.attrs['style'] = 'width: 5em'
        form.base_fields['message'].widget.attrs['style'] = 'width: 50em'
        return form

    def action(self, obj):
        return 'Modifier'

    def summary(self, obj):
        return obj.summary

    summary.short_description = 'Résumé'

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from teams.admin import ResultsAdminMixin

from .models import *
from teams.models import Team


@admin.register(Robotics1, Robotics2, Robotics3)
class RoboticScoreAdmin(admin.ModelAdmin, ResultsAdminMixin):
    class Media:
        js = ("js/hide_foreign_key_links.js",)

    list_display = ['verbose_team_name', 'get_points', 'get_detail']
    readonly_fields = ['time', 'get_points']
    ordering = ['team']

    class CustomChangeList(ChangeList):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title = "Sélectionnez le score à modifier"

    def get_changelist(self, request, **kwargs):
        return self.CustomChangeList

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Removes teams who have already participated to this round from the selector field. """
        if db_field.name == 'team':
            related_name = self.model.__name__.lower()
            kwargs['queryset'] = Team.objects.filter(**{'%s__isnull' % related_name: True})
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fields(self, request, obj=None):
        """ Removes the team selector field when updating and existing score. """
        fields = super().get_fields(request, obj)
        return fields if not obj else [f for f in fields if f != 'team']

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from teams.admin import ResultsAdminMixin

from .models import *


@admin.register(DocumentaryWork)
class DocumentaryWorkAdmin(admin.ModelAdmin, ResultsAdminMixin):
    list_display = ['verbose_team_name', 'get_points', 'get_detail']
    readonly_fields = ['time', 'get_points']
    fieldsets = (
        (None, {
            'fields': ('team', )
        }),
        ('Passage', {
            'fields': ('jury', 'done', 'time')
        }),
        ('Evaluation', {
            'fields': ('evaluation_available', 'topic_selection', 'documentation', 'presentation', 'expression', 'answers')
        }),
        ('Résumé', {
            'fields': ('get_points',)
        }),
    )

    class CustomChangeList(ChangeList):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title = "Sélectionnez l'évaluation à modifier"

    def get_changelist(self, request, **kwargs):
        return self.CustomChangeList

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['jury'].widget.attrs['style'] = 'width: 5em'
        return form


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin, ResultsAdminMixin):
    list_display = ['verbose_team_name', 'get_points', 'get_detail']
    readonly_fields = ['get_points']
    fieldsets = (
        (None, {
            'fields': ('team',)
        }),
        ('Evaluation', {
            'fields': ('conformity', 'quality', 'originality')
        }),
        ('Résumé', {
            'fields': ('get_points',)
        }),
    )

    class CustomChangeList(ChangeList):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title = "Sélectionnez l'évaluation à modifier"

    def get_changelist(self, request, **kwargs):
        return self.CustomChangeList

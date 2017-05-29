from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from .models import *


class VerboseTeamNameMixin(object):
    def verbose_team_name(self, obj):
        return obj.verbose_name

    verbose_team_name.short_description = "Equipe"


class ResultsAdminMixin(object):
    def verbose_team_name(self, obj):
        return obj.team.verbose_name

    verbose_team_name.short_description = "Equipe"

    def get_points(self, obj):
        return obj.get_points()

    get_points.short_description = 'points'

    def get_detail(self, obj):
        return obj.get_detail()

    get_detail.short_description = 'détail'


def check_in(modeladmin, request, queryset):
    queryset.update(present=True)

check_in.short_description = "Pointer les équipes sélectionnées"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin, VerboseTeamNameMixin):
    readonly_fields = ['num', 'match1_summary', 'match2_summary', 'match3_summary', 'research_summary',
                       'poster_summary']
    fieldsets = (
        (None, {
            'fields': ('num', 'name', 'school', 'grade_code', 'category_code', 'present')
        }),
        ('Robotique', {
            'fields': ('match1_summary', 'match2_summary', 'match3_summary')
        }),
        ('Exposé', {
            'fields': ('research_summary',)
        }),
        ('Poster', {
            'fields': ('poster_summary',)
        }),
    )
    list_display = ['verbose_team_name', 'unsortable_school', 'grade_abbrev', '_category', '_present']
    list_filter = ['category_code', 'school', 'school__city', 'present']
    ordering = None
    actions = [check_in]

    class CustomChangeList(ChangeList):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title = "Sélectionnez l'équipe à modifier"

    def get_changelist(self, request, **kwargs):
        return self.CustomChangeList

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['school'].widget.attrs['style'] = 'width: 30em'
        for field in ('category_code', 'grade_code'):
            form.base_fields[field].widget.attrs['style'] = 'width: 10em'
        return form

    def unsortable_school(self, obj: Team):
        return obj.school

    unsortable_school.short_description = 'Etablissement scolaire'

    def grade_abbrev(self, obj: Team):
        return obj.grade.abbrev

    grade_abbrev.short_description = 'Niveau'

    def match1_summary(self, obj: Team):
        return obj.robotics1.summary

    match1_summary.short_description = 'match 1'

    def match2_summary(self, obj: Team):
        return obj.robotics2.summary

    match2_summary.short_description = 'match 2'

    def match3_summary(self, obj: Team):
        return obj.robotics3.summary

    match3_summary.short_description = 'match 3'

    def research_summary(self, obj: Team):
        return obj.documentarywork.summary

    research_summary.short_description = 'évaluation'

    def poster_summary(self, obj: Team):
        return obj.poster.get_summary()

    poster_summary.short_description = 'évaluation'

    def _category(self, obj: Team):
        return obj.category.name

    _category.short_description = 'Catégorie'

    def _present(self, obj: Team):
        return obj.present

    _present.short_description = 'Présente'
    _present.boolean = True


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_filter = ['city']

    class CustomChangeList(ChangeList):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title = "Sélectionnez l'établissement scolaire à modifier"

    def get_changelist(self, request, **kwargs):
        return self.CustomChangeList

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field in ('name', 'city'):
            form.base_fields[field].widget.attrs['style'] = 'width: 30em'
        form.base_fields['zip_code'].widget.attrs['style'] = 'width: 5em'
        return form


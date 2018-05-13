from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db.models import DateField
from django.conf import settings

from suit.widgets import SuitDateWidget

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


class TeamMemberInlineModelAdmin(admin.TabularInline):
    model = TeamMember
    suit_classes = 'suit-tab suit-tab-members'
    formfield_overrides = {
        DateField: {
           'widget': SuitDateWidget
        }
    }

    class Media:
        css = {
            "all": ["/static/admin/css/team_member-inline.css"]
        }


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin, VerboseTeamNameMixin):
    readonly_fields = ['num', 'match1_summary', 'match2_summary', 'match3_summary', 'research_summary',
                       'poster_summary', 'average_age', 'grade_extent', 'complete']
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('num', 'name', 'school', 'category_code', 'contact', 'present', 'average_age', 'grade_extent')
        }),
        ('Robotique', {
            'classes': ('suit-tab', 'suit-tab-results'),
            'fields': ('match1_summary', 'match2_summary', 'match3_summary')
        }),
        ('Exposé', {
            'classes': ('suit-tab', 'suit-tab-results'),
            'fields': ('research_summary',)
        }),
        ('Poster', {
            'classes': ('suit-tab', 'suit-tab-results'),
            'fields': ('poster_summary',)
        }),
    )
    list_display = ['verbose_team_name', 'unsortable_school', '_category', '_present', '_complete']
    list_filter = ['category_code', 'school', 'school__city', 'present']
    ordering = None
    actions = [check_in]
    inlines = [TeamMemberInlineModelAdmin]
    suit_form_tabs = (
        ('general', 'Informations générales'),
        ('members', 'Composition'),
        ('results', 'Résultats'),
    )

    class CustomChangeList(ChangeList):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title = "Sélectionnez l'équipe à modifier"

    def get_changelist(self, request, **kwargs):
        return self.CustomChangeList

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['school'].widget.attrs['style'] = 'width: 30em'
        for field in ('category_code', ):
            form.base_fields[field].widget.attrs['style'] = 'width: 10em'
        return form

    def unsortable_school(self, obj: Team):
        return obj.school

    unsortable_school.short_description = 'Etablissement scolaire'

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

    def average_age(self, obj: Team):
        age = obj.average_age
        if age:
            years = int(age)
            months = round((age - years) * 12)
            if months == 12:
                years += 1
                months = 0
            if months:
                return "%d ans %d mois" % (years, months)
            else:
                return "%d ans" % years
        else:
            return '-'

    average_age.short_description = 'Age moyen'

    def grade_extent(self, obj: Team):
        extent = obj.grade_extent
        if extent:
            min_grade, max_grade = extent['min_grade'], extent['max_grade']     # type: Grade
            if min_grade == max_grade:
                return min_grade.name
            else:
                return f"{min_grade.abbrev} - {max_grade.abbrev}"
        else:
            return ""

    grade_extent.short_description = 'niveau scolaire'

    category_css_class = {
        Category.Mindstorms: 'info',
        Category.Arduino: 'success',
        Category.RaspberryPi: 'warning'
    }

    def suit_row_attributes(self, obj, request):
        return {'class': self.category_css_class[obj.category]}

    def _complete(self, obj: Team):
        return obj.complete

    _complete.short_description = 'Complète'
    _complete.boolean = True


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
        for field in ('name', 'address', 'city', 'email'):
            form.base_fields[field].widget.attrs['style'] = 'width: 30em'
        form.base_fields['zip_code'].widget.attrs['style'] = 'width: 5em'
        return form


class TeamInlineModelAdmin(admin.TabularInline):
    model = Team
    readonly_fields = fields = ['name']
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request):
        return False


def teamcontact_send_email_action(modeladmin, request, queryset):
    mail_to = ','.join((c.email for c in queryset))
    subject = '[PJC%s] ' % settings.PJC['edition']

    import webbrowser
    webbrowser.open('mailto:?to=%s&subject=%s' % (mail_to, subject.replace(' ', '%20')))


teamcontact_send_email_action.short_description = "Envoyer un email"


@admin.register(TeamContact)
class TeamContactAdmin(admin.ModelAdmin):
    inlines = [TeamInlineModelAdmin]
    list_display = ['__str__', 'school', 'email']
    actions = [teamcontact_send_email_action]

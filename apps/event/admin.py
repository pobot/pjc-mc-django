import datetime

from django.db.models import Min
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.conf.locale.fr import formats as fr_formats
from django.conf.locale.en import formats as en_formats
from .models import *

fr_formats.TIME_FORMAT = "H:i"
en_formats.TIME_FORMAT = "H:i"


class VerboseTeamNameMixin(object):
    def verbose_team_name(self, obj):
        return obj.team.verbose_name

    verbose_team_name.short_description = "Equipe"


@admin.register(Planning)
class TeamPlanningAdmin(admin.ModelAdmin, VerboseTeamNameMixin):
    list_display = ['verbose_team_name']

    class CustomChangeList(ChangeList):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title = "Sélectionnez le planning à modifier"

    def get_changelist(self, request, **kwargs):
        return self.CustomChangeList


@admin.register(PlanningControl)
class PlanningControlAdmin(admin.ModelAdmin, VerboseTeamNameMixin):
    list_display = ['verbose_team_name', 'match1_done', 'match2_done', 'match3_done', 'presentation_done']
    readonly_fields = list_display
    list_display_links = None

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        return []

    @staticmethod
    def status_display(done, schedule):
        return 'OK' if done else schedule.strftime('%H:%M')

    def match1_done(self, obj: Planning):
        return self.status_display(obj.match1_done, obj.match1_time)

    match1_done.short_description = 'Match 1'

    def match2_done(self, obj: Planning):
        return self.status_display(obj.match2_done, obj.match2_time)

    match2_done.short_description = 'Match 2'

    def match3_done(self, obj: Planning):
        return self.status_display(obj.match3_done, obj.match3_time)

    match3_done.short_description = 'Match 3'

    def presentation_done(self, obj: Planning):
        return self.status_display(obj.presentation_done, obj.presentation_time)

    presentation_done.short_description = 'Exposé'

    def suit_cell_attributes(self, obj: PlanningControl, column: str):
        if not column.endswith('_done'):
            return {}

        done = getattr(obj, column)
        if done:
            return {'class': 'text-success'}

        now = datetime.datetime.now()
        time_field = column.rsplit('_', 1)[0] + '_time'
        schedule = getattr(obj, time_field)
        abs_sched = datetime.datetime.combine(now.date(), schedule)
        if abs_sched < now:
            return {'class': 'text-error'}
        if abs_sched - now <= datetime.timedelta(minutes=15):
            return {'class': 'text-warning'}


class RankingCatFilter(admin.SimpleListFilter):
    title = 'classement'
    parameter_name = 'type_code'
    filter_allowed_values = [rt.value for rt in RankingType]
    default_value = RankingType.Scratch.value

    def lookups(self, request, model_admin):
        return ((rt.value, rt.name) for rt in RankingType)

    def queryset(self, request, queryset):
        try:
            v = int(self.value())
        except (ValueError, TypeError) as e:
            print(e)
            pass
        else:
            if v in self.filter_allowed_values:
                return queryset.filter(type_code=v)

        # return default ranking if no valid category is selected
        return queryset.filter(type_code=self.default_value)

    def value(self):
        value = super().value()
        return str(self.default_value) if value is None else value


@admin.register(Ranking)
class RankingDisplayAdmin(admin.ModelAdmin):
    list_display = ['team', 'team_cat', 'general', 'robotics', 'research', 'poster']
    readonly_fields = list_display
    list_filter = [RankingCatFilter]
    list_display_links = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_ranks_by_category = {}
        self.request = None

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        return []

    def team_cat(self, obj):
        return obj.team.category.name

    team_cat.short_description = 'catégorie'

    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)

        self.first_ranks_by_category = {
            None: qs.aggregate(
                general=Min('general'),
                robotics=Min('robotics'),
                research=Min('research'),
                poster=Min('poster'),
            )
        }
        for category in Category:
            qs_categ = qs.filter(team__category_code=category.value)
            if qs_categ:
                self.first_ranks_by_category[category] = qs_categ.aggregate(
                    general=Min('general'),
                    robotics=Min('robotics'),
                    research=Min('research'),
                    poster=Min('poster'),
                )
        return qs

    styles_columns = ('general', 'robotics', 'research', 'poster')

    def suit_cell_attributes(self, obj: Ranking, column: str):
        if column not in self.styles_columns:
            return {}

        attrs = {
            'class': 'text-center'
        }

        current_filter = self.request.GET.get('team__category_code__exact', None)
        category = Category(int(current_filter[0])) if current_filter else None
        first_ranks = self.first_ranks_by_category[category]

        if getattr(obj, column) == first_ranks[column]:
            attrs['style'] = 'color: #8a6d3b; background-color: #fcf8e3; font-weight: bold'

        return attrs

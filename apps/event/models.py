# -*- coding: utf-8 -*-

from collections import OrderedDict

import datetime
import arrow

from django.conf import settings
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from django.db import models as django_models
from django.core.exceptions import ValidationError


import suit.widgets

from teams.models import *
from match.models import *
from research.models import *

DEBUG_COMPUTE_RANKING = False

FORMFIELD_FOR_DBFIELD_DEFAULTS.update({
    django_models.TimeField: {'widget': suit.widgets.SuitTimeWidget},
})

PLANNING_SLOT_MINUTES = settings.PJC['planning_slot_minutes']
PLANNING_SLOT_SECONDS = PLANNING_SLOT_MINUTES * 60
SCHEDULE_MIN = arrow.get(settings.PJC['start_time'], 'HH:mm').time()
SCHEDULE_MAX = arrow.get(settings.PJC['end_time'], 'HH:mm').replace(seconds=-2 * PLANNING_SLOT_SECONDS).time()

time_validators = [
    validators.MinValueValidator(SCHEDULE_MIN, message=SCHEDULE_MIN.strftime("L'heure de passage doit être après %H:%M")),
    validators.MaxValueValidator(SCHEDULE_MAX, message=SCHEDULE_MAX.strftime("L'heure de passage doit être avant %H:%M")),
]

MSG_DELAY_TOO_SHORT = "écart de temps insuffisant"
MSG_DUPLICATE_TABLE = "tables identiques"

COMPETITION_ITEM_NAMES = [cls.__name__.lower() for cls in (Robotics1, Robotics2, Robotics3, DocumentaryWork, Poster)]


def time_dist(t1, t2):
    """
    :param datetime.time t1: 
    :param datetime.time t2: 
    :return: absolute distance between times (in seconds)
    :rtype: int 
    """
    return abs(
        datetime.timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second) -
        datetime.timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
    ).total_seconds()


TABLES = ['1', '2', '3']
TABLE_CHOICES = list(zip(TABLES, TABLES))


def validate_table(value):
    if value not in TABLES:
        raise ValidationError("numéro de table non valide (%s)" % value)

JURIES = ['1', '2', '3']
JURY_CHOICES = list(zip(JURIES, JURIES))


def validate_jury(value):
    if value not in JURIES:
        raise ValidationError("numéro de jury non valide (%s)" % value)


class Planning(TeamLinkedModel):
    class Meta:
        app_label = 'event'
        verbose_name = "planning équipe"
        ordering = ['team']

    match1_time = models.TimeField(
        verbose_name='horaire match 1',
        blank=False,
        validators=time_validators,
        default=SCHEDULE_MIN
    )
    match1_table = models.CharField(
        verbose_name='table match 1',
        max_length=1,
        blank=False,
        validators=[validate_table],
        choices=TABLE_CHOICES,
        default=TABLE_CHOICES[0][0]
    )
    match2_time = models.TimeField(
        verbose_name='horaire match 2',
        blank=False,
        validators=time_validators,
        default=SCHEDULE_MIN
    )
    match2_table = models.CharField(
        verbose_name='table match 2',
        max_length=1,
        blank=False,
        validators=[validate_table],
        choices=TABLE_CHOICES,
        default=TABLE_CHOICES[1][0]
    )
    match3_time = models.TimeField(
        verbose_name='horaire match 3',
        blank=False,
        validators=time_validators,
        default=SCHEDULE_MIN
    )
    match3_table = models.CharField(
        verbose_name='table match 3',
        max_length=1,
        blank=False,
        validators=[validate_table],
        choices=TABLE_CHOICES,
        default=TABLE_CHOICES[2][0]
    )
    presentation_time = models.TimeField(
        verbose_name='exposé',
        blank=False,
        validators=time_validators,
        default=SCHEDULE_MIN
    )
    jury = models.CharField(
        verbose_name='jury',
        max_length=1,
        blank=False,
        validators=[validate_jury],
        choices=JURY_CHOICES,
        default=JURY_CHOICES[0][0]
    )

    @property
    def match1_done(self):
        return Robotics1.objects.filter(team__pk=self.team.pk).exists()

    @property
    def match2_done(self):
        return Robotics2.objects.filter(team__pk=self.team.pk).exists()

    @property
    def match3_done(self):
        return Robotics3.objects.filter(team__pk=self.team.pk).exists()

    @property
    def presentation_done(self):
        return DocumentaryWork.objects.filter(team__pk=self.team.pk).exists()

    @property
    def match_times(self):
        return [self.match1_time, self.match2_time, self.match3_time]

    @property
    def times(self):
        return self.match_times + [self.presentation_time]

    @property
    def match_tables(self):
        return [self.match1_table, self.match2_table, self.match3_table]

    @property
    def locations(self):
        return self.match_tables + [self.jury]

    @property
    def done(self):
        return [self.match1_done, self.match2_done, self.match3_done, self.presentation_done]

    @property
    def ending_times(self):
        return [
            time_add_minutes(t, PLANNING_SLOT_MINUTES) if i < 3 else time_add_minutes(t, 3 * PLANNING_SLOT_MINUTES)
            for i, t in enumerate(self.times)
        ]

    @property
    def time_span(self):
        return min(self.times), max(self.ending_times)

    def clean(self):
        match_times = self.times[:3]
        for m1, m2 in [(0, 1), (1, 2), (0, 2)]:
            t1, t2 = (match_times[i] for i in (m1, m2))
            if time_dist(t1, t2) < PLANNING_SLOT_SECONDS:
                raise ValidationError({'match%d_time' % (n+1): MSG_DELAY_TOO_SHORT for n in (m1, m2)})

        for i, m in enumerate(match_times):
            if time_dist(self.presentation_time, m) < PLANNING_SLOT_SECONDS:
                raise ValidationError({
                    'match%d_time' % (i+1): MSG_DELAY_TOO_SHORT,
                    'presentation_time': MSG_DELAY_TOO_SHORT
                })

        tables = self.locations[:3]
        if len(set(tables)) != 3:
            for table in TABLES:
                matches = [n for n, t in enumerate(tables) if t == table]
                if len(matches) > 1:
                    raise ValidationError({
                        'match%d_table' % n: MSG_DUPLICATE_TABLE for n in matches
                    })

    def next_schedule(self, from_time=None):
        if from_time is None:
            # from_time = arrow.now().time()
            from_time = SCHEDULE_MIN
        what = ['épreuve %d' % (i + 1) if i <= 2 else 'exposé' for i in range(len(self.times))]
        next_schedules = [
            (t, l, w) for t, l, w, done in zip(self.times, self.locations, what, self.done)
            if t >= from_time and not done
        ]
        return min(next_schedules) if next_schedules else None

    def verbose(self):
        return " ".join([
            "%s(%s,%s)" % (what, time.strftime('%H:%M'), loc)
            for what, time, loc in zip(('M1', 'M2', 'M3', 'EXP'), self.times, self.locations)
        ])


def time_add_minutes(t, minutes):
    m = t.minute + minutes
    dh = m // 60
    return datetime.time(hour=t.hour + dh, minute=m % 60)


class PlanningControl(Planning):
    """ Proxy model for the planning. 
    
    We need it to be able to display the planning differently in the progression control admin page, since Django
    admin cannot register the same model in two different ModelAdmins. 
    """
    class Meta:
        app_label = 'event'
        proxy = True
        verbose_name = 'Avancement'
        verbose_name_plural = 'Avancement'


class RankingType(Enum):
    Scratch = 0
    Mindstorms = Category.Mindstorms.value
    Arduino = Category.Arduino.value
    RaspberryPi = Category.RaspberryPi.value


class Ranking(models.Model):
    class Meta:
        app_label = 'event'
        verbose_name = "classement"
        unique_together = ['type_code', 'team']
        ordering = ['type_code', 'team']

    type_code = models.PositiveSmallIntegerField(
        verbose_name='type classement',
        choices=[(rt.value, rt.name) for rt in RankingType],
        default=RankingType.Scratch.value
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name='équipe'
    )
    general = models.PositiveSmallIntegerField(
        verbose_name='classement général',
        blank=False,
        default=0
    )
    robotics = models.PositiveSmallIntegerField(
        verbose_name='classement robotique',
        blank=False,
        default=0
    )
    research = models.PositiveSmallIntegerField(
        verbose_name='classement recherche',
        blank=False,
        default=0
    )
    poster = models.PositiveSmallIntegerField(
        verbose_name='classement poster',
        blank=False,
        default=0
    )

    def __str__(self):
        return "categ:{self.type_code} gen:{self.general} rob:{self.robotics} doc:{self.research} pos:{self.poster}".\
            format(self=self)

    @classmethod
    def compute_typed_ranking(cls, teams, ranking_type, verbose=False):
        # results:
        #   team : [pts(rob1), pts(rob2), pts(rob3), pts(research), pts(poster)]
        results = OrderedDict((
            (t, [points_or_forfait(t, item) for item in COMPETITION_ITEM_NAMES]) for t in teams
        ))
        if verbose:
            _print_raw_results(results, ranking_type)

        # compute the ranking points as a matrix arranged by topic first
        # rp_raw:
        #   rob1     -> [rp(t1), rp(t2),... ]
        #   rob2     -> [rp(t1), rp(t2),... ]
        #   rob3     -> [rp(t1), rp(t2),... ]
        #   research -> [rp(t1), rp(t2),... ]
        #   poster   -> [rp(t1), rp(t2),... ]
        rp_raw = [to_rank_points(pts) for pts in transposed(results.values())]
        if verbose:
            _print_raw_rank_points_results(rp_raw, ranking_type)

        # merge robotics ranking points by summing the first 3 rows
        # intermediate_raw_rp:
        #   rob      -> [rp(t1), rp(t2),... ]
        #   research -> [rp(t1), rp(t2),... ]
        #   poster   -> [rp(t1), rp(t2),... ]
        intermediate_raw_rp = list(transposed([[sum(l[0:3]), l[3], l[4]] for l in transposed(rp_raw)]))
        if verbose:
            _print_merged_rank_points_results(intermediate_raw_rp, ranking_type)

        # separate ex-aequos for research and poster

        ages = [t.average_age for t in teams]

        def _separate_first_rank_ex_aequos(row):
            rp = list(intermediate_raw_rp[row])
            # get the highest rank point, which is associated to the first team
            rp_first = max(rp)
            # find all ex-aequos
            ex_aequos = [i for i in range(len(rp)) if rp[i] == rp_first]
            if len(ex_aequos) > 1:
                # if some, get the lowest team age
                min_age = min([ages[i] for i in ex_aequos])
                # select the youngest team
                youngest_team = [i for i in ex_aequos if ages[i] == min_age][0]
                # push the others one rank backwards by reducing their rank points
                for team in ex_aequos:
                    if team != youngest_team:
                        rp[team] = rp[team] - 1

                intermediate_raw_rp[row] = rp

        for i in (1, 2):    # research, poster
            _separate_first_rank_ex_aequos(i)

        # compute the rankings per team and save it for later
        # ranking_data:
        #   team : [0, rank(rob), rank(research), rank(poster)]
        ranking_data = {
            t: [0] + list(r)  # pre-allocate the first slot for the general rank which will be computed later
            for t, r in zip(results.keys(), transposed(to_ranks(rp) for rp in intermediate_raw_rp))
        }
        if verbose:
            _print_rankings(ranking_data, ranking_type)

        # normalize to ranking points
        intermediate_rp = [to_rank_points(rp) for rp in intermediate_raw_rp]
        # print('intermediate_rp =', intermediate_rp)

        # compute the global ranking
        global_ranking = to_ranks([sum(l) for l in zip(*intermediate_rp)])
        # if verbose:
        #     print('global_ranking =', global_ranking)

        # differentiate 1st position ex-aequo by using the team average age

        # 1. create the map (rank -> list of teams at this rank)
        by_rank = {
            g_r: [t for t, t_r in zip(results.keys(), global_ranking) if t_r == g_r]
            for g_r in global_ranking
        }
        if verbose:
            _print_by_rank(by_rank, ranking_type)

        # 2. get the teams at first rank
        teams = by_rank[1]
        if len(teams) > 1:
            # if more than one, sort them by the average age, first one being the youngest
            teams.sort(key=lambda t: t.average_age)
            # keep the first one at first rank
            by_rank[1] = teams[:1]
            # and push the others at rank 2
            by_rank[2] = teams[1:]

            if verbose:
                _print_by_rank(by_rank, ranking_type, ex_aequo_removed=True)

        # finally, update the global rank of each team with the one we just computed
        for r, teams in by_rank.items():
            for t in teams:
                ranking_data[t][0] = r

        # and save the result in the db
        ranks = [
            Ranking(type_code=ranking_type, team=t,
                    general=r[0], robotics=r[1], research=r[2], poster=r[3]
                    )
            for t, r in ranking_data.items()
        ]
        # _print_rankings(ranks, ranking_type, final=True)

        cls.objects.bulk_create(ranks)

    @classmethod
    def compute(cls, verbose=False):
        cls.objects.all().delete()
        if verbose:
            print("Ranking dataset cleared")

        for ranking_type in RankingType:
            if ranking_type != RankingType.Scratch:
                teams = Team.objects.filter(present=True, category_code=ranking_type.value)
            else:
                teams = Team.objects.filter(present=True)
            if teams:
                if verbose:
                    print("[%-15s] --- ranking computation started" % ranking_type.name)
                cls.compute_typed_ranking(teams, ranking_type.value, verbose)
                if verbose:
                    print("[%-15s] --- ranking computation complete" % ranking_type.name)
            else:
                if verbose:
                    print("[%-15s] !!! no team for this category" % ranking_type.name)


def points_or_forfait(team, item_name):
    try:
        item = getattr(team, item_name)
    except AttributeError:
        return -1
    else:
        return item.get_points()


def to_ranks(teams_pts):
    """ 
    Given a list of points ordered by team, returns the corresponding list of ranks.

    :param [list|tuple] teams_pts: teams points
    :return: ranking of teams for the provided points
    :rtype: list
    """
    sorted_points = list(reversed(sorted(teams_pts)))
    return [sorted_points.index(pts) + 1 for pts in teams_pts]


def to_rank_points(teams_pts):
    """
    Given a list of points ordered by team, returns the corresponding list of ranking points.

    Teams not having participated to a given item are credited no point for it.

    :param [list|tuple] teams_pts: teams points
    :return: ranking points
    :rtype: list
    """
    return [(len(teams_pts) + 1 - rank) if pts >= 0 else 0 for rank, pts in zip(to_ranks(teams_pts), teams_pts)]


def transposed(m):
    return zip(*m)


def _print_raw_results(points, ranking_type):
    if not points:
        return

    print('[%s] raw results per team :' % RankingType(ranking_type).name)
    lines = [
        '... {team.verbose_name:30s} - {points}'.format(team=team, points=raw_points)
        for team, raw_points in points.items()
    ]
    print('\n'.join(lines))


def _print_raw_rank_points_results(points, ranking_type):
    if not points:
        return

    print('[%s] raw rank points per item :' % RankingType(ranking_type).name)
    lines = [
        '... {item:30s} - {points}'.format(item=COMPETITION_ITEM_NAMES[i], points=raw_points)
        for i, raw_points in enumerate(points)
    ]
    print('\n'.join(lines))


def _print_merged_rank_points_results(points, ranking_type):
    if not points:
        return

    item_names = ['robotics'] + COMPETITION_ITEM_NAMES[3:]
    print('[%s] merged rank points :' % RankingType(ranking_type).name)
    lines = [
        '... {item:30s} - {points}'.format(item=item_names[i], points=raw_points)
        for i, raw_points in enumerate(points)
    ]
    print('\n'.join(lines))


def _print_rankings(data, ranking_type, final=False):
    if not data:
        return

    print('[%s] %s rankings per team :' % (RankingType(ranking_type).name, 'final' if final else 'intermediate'))
    lines = [
        '... {team.verbose_name:30s} - {data}'.format(team=t, data=ranking_data)
        for t, ranking_data in data.items()
    ]
    print('\n'.join(lines))


def _print_by_rank(data, ranking_type, ex_aequo_removed=False):
    if not data:
        return

    print('[%s] teams by rank %s:' % (RankingType(ranking_type).name, '(ex-aequo removed)' if ex_aequo_removed else ''))
    lines = [
        '... {rank:2d} - {teams}'.format(rank=rank, teams=teams)
        for rank, teams in data.items()
    ]
    print('\n'.join(lines))

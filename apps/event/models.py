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
    def compute(cls):
        def compute_typed_ranking(teams, ranking_type):
            results = OrderedDict((
                (t, (
                    t.robotics1.get_points(),
                    t.robotics2.get_points(),
                    t.robotics3.get_points(),
                    t.documentarywork.get_points(),
                    t.poster.get_points()
                )) for t in teams
            ))
            # print('results =', results)

            # compute the ranking points as a matrix arranged by topic first
            rp_raw = [to_rank_points(pts) for pts in transposed(results.values())]
            # print('rp_raw =', rp_raw)

            # merge robotics ranking points by summing the first 3 rows
            intermediate_raw_rp = list(transposed(((sum(l[0:3]), l[3], l[4]) for l in transposed(rp_raw))))
            # print('intermediate_raw_rp =', intermediate_raw_rp)

            # compute the rankings per rows and save it for later
            ranking_data = {
                t: [0] + list(r)  # save first place for general rank which will be computed later
                for t, r in zip(results.keys(), transposed(to_ranks(rp) for rp in intermediate_raw_rp))
            }
            # print('ranking_data =', ranking_data)

            # normalize to ranking points
            intermediate_rp = [to_rank_points(rp) for rp in intermediate_raw_rp]
            # print('intermediate_rp =', intermediate_rp)

            # compute the global ranking
            global_ranking = to_ranks([sum(l) for l in zip(*intermediate_rp)])
            # print('global_ranking =', global_ranking)

            # differentiate ex-aequo by using the team age bonus
            by_rank = {
                g_r: [t for t, t_r in zip(results.keys(), global_ranking) if t_r == g_r]
                for g_r in global_ranking
            }
            for r, teams in by_rank.items():
                if len(teams) > 1:
                    teams.sort(key=lambda t: t.grade.bonus, reverse=True)
                for n, t in enumerate(teams):
                    ranking_data[t][0] = r + n

            ranks = [
                Ranking(type_code=ranking_type, team=t,
                        general=r[0], robotics=r[1], research=r[2], poster=r[3]
                        )
                for t, r in ranking_data.items()
            ]
            # print('ranks =', ranks)

            # save the result in the db
            cls.objects.bulk_create(ranks)

        cls.objects.all().delete()
        # print("Ranking dataset cleared")

        for ranking_type in RankingType:
            if ranking_type != RankingType.Scratch:
                teams = Team.objects.indexable().filter(category_code=ranking_type.value)
            else:
                teams = Team.objects.indexable()
            compute_typed_ranking(teams, ranking_type.value)
            # print("%s ranking computed" % ranking_type)


def to_ranks(teams_pts):
    """ 
    Given a list of points ordered by team, returns the corresponding list of ranks.

    :param list teams_pts: teams points
    :return: ranking of teams for the provided points
    :rtype: list
    """
    sorted_points = list(reversed(sorted(teams_pts)))
    return [sorted_points.index(pts) + 1 for pts in teams_pts]


def to_rank_points(teams_pts):
    """
    Given a list of points ordered by team, returns the corresponding list of rank ing points.
    :param list teams_pts: teams points
    :return: ranking points
    :rtype: list
    """
    return [len(teams_pts) + 1 - rank for rank in to_ranks(teams_pts)]


def transposed(m):
    return zip(*m)



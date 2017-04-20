# -*- coding: utf-8 -*-

from collections import namedtuple
from enum import Enum

from django.db import models
from django.core import validators
from django.contrib.auth.models import User


GradeProps = namedtuple('GradeProps', 'name abbrev bonus db_value')


class Grade(Enum):
    post_bac = ('PostBAC', '>BAC', 0)
    terminale = ('Terminale', 'Tale', 1)
    premiere = ('Première', '1ère', 2)
    seconde = ('Seconde', '2nde', 3)
    troisieme = ('Troisième', '3ème', 4)
    quatrieme = ('Quatrième', '4ème', 5)
    cinquieme = ('Cinquième', '5ème', 6)
    sixieme = ('Sixième', '6ème', 7)
    cm2 = ('CM2', 'CM2', 8)
    cm1 = ('CM1', 'CM1', 9)

    def __init__(self, label, abbrev, bonus):
        self.label = label
        self.abbrev = abbrev
        self.bonus = bonus
        self.db_value = len(self.__class__.__members__) + 1

        if not hasattr(self.__class__, '_index'):
            self.__class__._index = {}
        self._index[self.db_value] = self

    @classmethod
    def by_db_value(cls, v):
        return cls._index[v]


class Category(Enum):
    Mindstorms = 1
    Arduino = 2
    RaspberryPi = 3


class TeamManager(models.Manager):
    def indexable(self):
        return super().get_queryset().filter(
            robotics1__isnull=False,
            robotics2__isnull=False,
            robotics3__isnull=False,
            documentarywork__isnull=False,
            poster__isnull=False
        ).exclude(documentarywork__evaluation_available=False)


class Team(models.Model):
    class Meta:
        app_label = 'teams'
        verbose_name = "équipe"
        ordering = ['num']

    objects = TeamManager()

    num = models.AutoField(
        verbose_name="numéro",
        primary_key=True
    )
    name = models.CharField(
        verbose_name="nom",
        max_length=20,
        blank=False,
        unique=True
    )
    school = models.ForeignKey(
        'School',
        verbose_name='établissement scolaire',
        blank=True,
        null=True,
        related_name='teams',
        on_delete=models.PROTECT
    )
    grade_code = models.SmallIntegerField(
        verbose_name="niveau scolaire",
        choices=[(g.db_value, g.label) for g in Grade],
        default=Grade.sixieme.db_value
    )
    category_code = models.SmallIntegerField(
        verbose_name="catégorie",
        choices=[(c.value, c.name) for c in Category],
        default=Category.Mindstorms.value
    )
    present = models.BooleanField(
        verbose_name="présente",
        default=False
    )

    @property
    def grade(self):
        return Grade.by_db_value(self.grade_code)

    @grade.setter
    def grade(self, grade_enum):
        self.grade_code = grade_enum.db_value

    @property
    def category(self):
        return Category(self.category_code)

    @category.setter
    def category(self, category_enum):
        self.category_code = category_enum.value

    def __str__(self):
        return self.verbose_name

    @property
    def verbose_name(self):
        return "{self.num:2} - {self.name}".format(self=self)


class School(models.Model):
    class Meta:
        app_label = 'teams'
        verbose_name = "établissement scolaire"
        verbose_name_plural = "établissements scolaires"
        ordering = ['zip_code', 'name']

    name = models.CharField(
        verbose_name="nom",
        max_length=50,
        blank=False,
    )
    city = models.CharField(
        verbose_name="ville",
        max_length=50,
        blank=False,
    )
    zip_code = models.CharField(
        verbose_name="code postal",
        max_length=5,
        blank=False,
        validators=[validators.RegexValidator(r'^[0-9]{5}$', message='Code postal invalide')]
    )

    def __str__(self):
        return "{self.name} ({self.city})".format(self=self)


class TeamLinkedModel(models.Model):
    class Meta:
        abstract = True

    team = models.OneToOneField(
        Team,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='équipe',
        error_messages={
            'unique': "Résultat déjà saisi pour cette équipe."
        }
    )

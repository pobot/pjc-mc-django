# -*- coding: utf-8 -*-

from collections import namedtuple
from enum import Enum
import datetime
from statistics import mean

from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django.db.models.aggregates import Max, Min


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


class UpperCasedField(models.CharField):
    description = "A CharField containing an automatically upper cased value"

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value.upper() if value else value


class LastNameField(UpperCasedField):
    description = "An UpperCasedField with sensible defaults for the last name of somebody"

    def __init__(self, *args, **kwargs):
        verbose_name = kwargs.pop('verbose_name', 'nom')
        max_length = kwargs.pop('max_length', 30)
        super().__init__(*args, verbose_name=verbose_name, max_length=max_length, **kwargs)


class FirstNameField(models.CharField):
    description = "A CharField containing a capitalized first name"

    def __init__(self, *args, **kwargs):
        verbose_name = kwargs.pop('verbose_name', 'prénom')
        max_length = kwargs.pop('max_length', 30)
        super().__init__(*args, verbose_name=verbose_name, max_length=max_length, **kwargs)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value.title() if value else value


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
    category_code = models.SmallIntegerField(
        verbose_name="catégorie",
        choices=[(c.value, c.name) for c in Category],
        default=Category.Mindstorms.value
    )
    contact = models.ForeignKey(
        'TeamContact',
        verbose_name='contact',
        # blank=False,
        null=True,
        related_name='teams',
        on_delete=models.PROTECT
    )
    present = models.BooleanField(
        verbose_name="présente",
        default=False
    )

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

    @property
    def grade_extent(self):
        # TODO cache this by making it a read-only fields pair, updated on members changes
        # Grade codes are defined in the reverse order of the grade itself, so that the can be used as bonus for
        # the youngest competitors. This is why the min grade is given by the max of the grade code.
        if self.members.exists():
            return {
                k: Grade.by_db_value(v)
                for k, v in self.members.all().aggregate(min_grade=Max('grade_code'), max_grade=Min('grade_code')).items()
            }
        else:
            return None

    @property
    def grade_extent_display(self):
        extent = self.grade_extent
        if extent:
            min_grade, max_grade = extent['min_grade'], extent['max_grade']     # type: Grade
            if min_grade == max_grade:
                return min_grade.abbrev
            else:
                return f"{min_grade.abbrev} à {max_grade.abbrev}"
        else:
            return ""

    @property
    def average_age(self):
        # TODO cache this by making it a read-only field, updated on members changes
        if self.members.exists():
            return mean(m.age for m in self.members.all())
        else:
            return 0

    @property
    def complete(self):
        return self.members.count() > 0


class TeamMember(models.Model):
    class Meta:
        app_label = 'teams'
        verbose_name = "équipier"
        verbose_name_plural = "équipiers"
        unique_together = ['first_name', 'last_name']

    team = models.ForeignKey(
        'Team',
        verbose_name='équipe',
        related_name='members',
        on_delete=models.PROTECT
    )
    first_name = FirstNameField(
        blank=False,
    )
    last_name = LastNameField(
        blank=False,
    )
    birth_date = models.DateField(
        verbose_name="date de naissance",
        blank=False
    )
    grade_code = models.SmallIntegerField(
        verbose_name="niveau scolaire",
        choices=[(g.db_value, g.label) for g in Grade],
        default=Grade.sixieme.db_value
    )

    @property
    def grade(self):
        return Grade.by_db_value(self.grade_code)

    @grade.setter
    def grade(self, grade_enum):
        self.grade_code = grade_enum.db_value

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.first_name.title() + ' ' + self.last_name.upper()

    @property
    def age(self):
        return (datetime.date.today() - self.birth_date).days / 365


class TeamContact(models.Model):
    class Meta:
        app_label = 'teams'
        verbose_name = "contact"
        verbose_name_plural = "contacts"
        ordering = ['last_name']

    gender = models.CharField(
        verbose_name="genre",
        max_length=4,
        choices=[('M', 'M'), ('Mme', 'Mme'), ('Mlle', 'Mlle')],
        default='M',
        blank=False
    )
    first_name = FirstNameField(
        blank=False,
    )
    last_name = LastNameField(
        blank=False,
    )
    email = models.EmailField(
        verbose_name="email",
        max_length=150,
        blank=True,
    )
    phone_number = models.CharField(
        verbose_name="téléphone",
        max_length=20,
        blank=True,
    )
    school = models.ForeignKey(
        'School',
        verbose_name='établissement scolaire',
        blank=True,
        null=True,
        related_name='contacts',
        on_delete=models.PROTECT
    )
    taught_subject = models.CharField(
        verbose_name='matière enseignée',
        max_length=20,
        blank=True
    )

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.first_name.title() + ' ' + self.last_name.upper()


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
    address = models.CharField(
        verbose_name="adresse",
        max_length=250,
        blank=True,
    )
    city = UpperCasedField(
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
    email = models.EmailField(
        verbose_name="email",
        max_length=150,
        blank=True,
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
            'unique': "Données déjà saisies pour cette équipe."
        }
    )

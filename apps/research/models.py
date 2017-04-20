# -*- coding: utf-8 -*-

from django.db import models

from teams.models import TeamLinkedModel

EVALUATION_CHOICES = (
    (0, '0 - insuffisant'),
    (1, '1 - médiocre'),
    (2, '2 - moyen'),
    (3, '3 - bien'),
    (4, '4 - très bien')
)


class DocumentaryWork(TeamLinkedModel):
    class Meta:
        app_label = 'research'
        verbose_name = "exposé"
        ordering = ['team']

    jury = models.PositiveSmallIntegerField(
        verbose_name='jury',
        choices=((i, i) for i in range(1, 4)),
        default=1,
    )
    time = models.TimeField(
        verbose_name='heure de passage',
        auto_now_add=True,
    )
    topic_selection = models.PositiveSmallIntegerField(
        verbose_name='pertinence du sujet',
        choices=EVALUATION_CHOICES,
        default=0
    )
    documentation = models.PositiveSmallIntegerField(
        verbose_name='travail de documentation',
        choices=EVALUATION_CHOICES,
        default=0
    )
    presentation = models.PositiveSmallIntegerField(
        verbose_name='qualité de la présentation',
        choices=EVALUATION_CHOICES,
        default=0
    )
    expression = models.PositiveSmallIntegerField(
        verbose_name='expression orale',
        choices=EVALUATION_CHOICES,
        default=0
    )
    answers = models.PositiveSmallIntegerField(
        verbose_name='réponses aux questions',
        choices=EVALUATION_CHOICES,
        default=0
    )
    done = models.BooleanField(
        verbose_name='fait',
        default=False
    )
    evaluation_available = models.BooleanField(
        verbose_name='évaluation disponible',
        default=False
    )

    def __str__(self):
        return self.team.name

    def get_points(self):
        return self.topic_selection + self.documentation + self.presentation + self.expression + self.answers

    points = property(get_points)

    def get_detail(self):
        if self.evaluation_available:
            return "sujet : {self.topic_selection}, recherche : {self.documentation}, " \
                   "présentation : {self.presentation}, expression : {self.expression}, questions : {self.answers}"\
                .format(self=self)
        else:
            return "évaluation non disponible"

    detail = property(get_detail)

    @property
    def summary(self):
        if self.evaluation_available:
            return "{points} pts ({detail})".format(points=self.get_points(), detail=self.get_detail())
        else:
            return "évaluation non disponible"


class Poster(TeamLinkedModel):
    class Meta:
        app_label = 'research'
        verbose_name = "poster"
        ordering = ['team']

    conformity = models.PositiveSmallIntegerField(
        verbose_name='conformité',
        choices=EVALUATION_CHOICES,
        default=0
    )
    quality = models.PositiveSmallIntegerField(
        verbose_name='réalisation',
        choices=EVALUATION_CHOICES,
        default=0
    )
    originality = models.PositiveSmallIntegerField(
        verbose_name='originalité',
        choices=EVALUATION_CHOICES,
        default=0
    )

    def __str__(self):
        return self.team.name

    def get_points(self):
        return self.conformity + self.quality + self.originality

    def get_detail(self):
        return "conformité : {self.conformity}, réalisation : {self.quality}, originalité : {self.originality}"\
            .format(self=self)

    def get_summary(self):
        return "{points} pts ({detail}".format(points=self.get_points(), detail=self.get_detail())

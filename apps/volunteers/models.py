# -*- coding: utf-8 -*-

from django.db import models

from share.fields import LastNameField, FirstNameField

__author__ = 'Eric Pascual'


class Volunteer(models.Model):
    class Meta:
        app_label = 'volunteers'
        verbose_name = "volontaire"
        verbose_name_plural = "volontaires"
        ordering = ['last_name']
        unique_together = ('first_name', 'last_name')

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
    )
    status = models.CharField(
        verbose_name='réponse',
        max_length=1,
        choices=[('?', 'pas de réponse'), ('O', 'OK'), ('N', 'non disponible')],
        default='?',
    )
    present = models.BooleanField(
        verbose_name='présent(e)',
        default=False
    )
    notes = models.TextField(
        verbose_name='notes',
        blank=True
    )

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.first_name.title() + ' ' + self.last_name.upper()

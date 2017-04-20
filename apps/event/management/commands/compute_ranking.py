# -*- coding: utf-8 -*-

from django.core.management import BaseCommand

from event.models import Ranking

__author__ = 'Eric Pascual'


class Command(BaseCommand):
    def handle(self, *args, **options):
        Ranking.compute()

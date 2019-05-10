# -*- coding: utf-8 -*-

from django.core.management import BaseCommand

from teams.models import Team
from match.models import Robotics1, Robotics2, Robotics3
from research.models import DocumentaryWork, Poster
from event.models import Ranking

__author__ = 'Eric Pascual'


class Command(BaseCommand):
    @staticmethod
    def _humanized_rows_count(count):
        if count == 0:
            return "no row"
        if count == 1:
            return "1 row"
        return "%s rows" % count

    def handle(self, *args, **options):
        self.stdout.write("""
        WARNING !!!
        
        This command resets the data to the contest starting state. All match results and evaluations
        will be deleted, and the team presence status will be reset to False.
        
        This action CANNOT BE UNDONE.
        """)
        confirm = input("Enter 'YES' to confirm: ")
        if confirm != 'YES':
            self.stdout.write('Command canceled. No data has been changed.')
            return

        for model in (Robotics1, Robotics2, Robotics3, DocumentaryWork, Poster, Ranking):
            deleted, _ = model.objects.all().delete()
            self.stdout.write('- %s model : %s deleted' % (
                model.__name__, self._humanized_rows_count(deleted)
            ))

        updated = Team.objects.filter(present=True).update(present=False)
        self.stdout.write('- Teams presence : %s updated' % self._humanized_rows_count(updated))

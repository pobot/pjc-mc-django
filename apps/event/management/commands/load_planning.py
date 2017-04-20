# -*- coding: utf-8 -*-

import datetime
import csv
from itertools import cycle

from django.core.management import BaseCommand

from teams.models import Team
from event.models import TABLES, JURIES, Planning

__author__ = 'Eric Pascual'


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=open, help="CSV file to load")

    def handle(self, *args, **options):
        fp = options['csv_file']

        fp.seek(0)
        rdr = csv.reader(fp)

        x0 = 2
        cells = next(rdr)
        for x0, time_slot in enumerate(cells):
            if time_slot:
                break
        time_slots = [datetime.datetime.strptime(t, "%H:%M").time() for t in cells[x0:]]

        # process team lines
        table_cycle = cycle(TABLES)
        jury_cycle = cycle(JURIES)
        plannings = []

        in_teams = False
        for cells in rdr:
            team_num = cells[0]
            if team_num:
                in_teams = True
                team = Team.objects.get(num=team_num)
                planning_cells = cells[x0:]
                slots_indices = [planning_cells.index(s) for s in ('M1', 'M2', 'M3', 'EXP')]
                planning = Planning(team=team)
                for i, ndx in enumerate(slots_indices):
                    t = time_slots[ndx]
                    if i < 3:
                        setattr(planning, 'match%d_time' % (i + 1), t)
                        setattr(planning, 'match%d_table' % (i + 1), next(table_cycle))
                    else:
                        planning.presentation_time = t
                        planning.jury = next(jury_cycle)

                # rotate the table so that we go to the next table for the next team of the same round
                next(table_cycle)
                self.stdout.write("{team:30} - {planning}".format(team=team.verbose_name, planning=planning.verbose()))
                plannings.append(planning)

            elif in_teams:
                break

        Planning.objects.all().delete()
        Planning.objects.bulk_create(plannings)

# -*- coding: utf-8 -*-

from textwrap import dedent
import argparse
import os

from django.core.management import BaseCommand


__author__ = 'Eric Pascual'

SCRIPT_HOME = os.path.dirname(__file__)

_generators = {
    'm': (generate_match_sheets, 'match sheets', 'match_sheets', portrait(A4)),
    'j': (generate_jury_sheets, 'jury sheets', 'jury_sheets', portrait(A4)),
    'a': (generate_approval_sheets, 'approval sheets', 'approval_sheets', portrait(A4)),
    's': (generate_stand_labels, 'stand labels', 'stand_labels', portrait(A4)),
    'p': (generate_planning, 'planning', 'planning', landscape(A4)),
    'l': (generate_teams_list, 'teams list', 'teams_list', portrait(A4)),
    'x': (generate_signs, 'signs', 'signs', landscape(A4)),
}


all_types = ''.join(_generators.keys())


def output_dir(value):
    path = os.path.abspath(os.path.join(SCRIPT_HOME, value))
    if os.path.exists(path) and not os.path.isdir(path):
        raise argparse.ArgumentTypeError('path exists and is not a directory (%s)' % path)
    return path


def doc_types(value):
    if value == '*':
        return all_types

    value = value.lower()
    if any(c not in all_types for c in value):
        raise argparse.ArgumentTypeError("invalid code used in document types list")
    return value


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.description=dedent("""
            Event forms and documents generator.

            Produces the PDF files for the various forms and documents personalized
            with the team information.

            Which documents are generated can be customized with the -g/--generate options.
            Its value is either '*' meaning 'all' or a case insensitive string of
            one letter codes representing the document types.

            Available documents are (document code given in parenthesis):
                - (a) individual approval sheets
                - (j) individual jury sheets for the presentation evaluations
                - (l) teams list
                - (m) individual match sheets for score accounting
                - (p) global planning
                - (s) stand labels
                - (t) individual time tables
                - (x) signs for tables and jury rooms
        """),
        parser.formatter_class=argparse.RawTextHelpFormatter

        parser.add_argument('-o', '--output_dir',
                            help='output directory, created if not found\n(default: "%(default)s")',
                            type=output_dir,
                            default='./output')
        parser.add_argument('-g', '--generate',
                            dest='doctypes',
                            help='specify which documents are to be generated\n(default: "%(default)s")',
                            type=doc_types,
                            default=all_types)

    def handle(self, *args, **options):
        pass

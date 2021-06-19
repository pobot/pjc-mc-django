# -*- coding: utf-8 -*-

from textwrap import dedent
import argparse
import os

from django.core.management import BaseCommand

from docmaker.generators.approval_forms import ApprovalFormGenerator
from docmaker.generators.jury_forms import JuryFormGenerator
from docmaker.generators.stand_labels import StandLabelGenerator
from docmaker.generators.planning import PlanningGenerator
from docmaker.generators.teams_list import TeamsListGenerator
from docmaker.generators.signs import SignsGenerator
from docmaker.generators.match_forms import RoboticsMatchFormGenerator
from docmaker.generators.diplomas import DiplomasGenerator
from docmaker.generators.poster_evaluation import PostersEvalGridGenerator
from docmaker.generators.team_registration_form import TeamRegistrationFormGenerator

from docmaker.commons import GenerationError

__author__ = 'Eric Pascual'

SCRIPT_HOME = os.path.dirname(__file__)

_generators = {
    'j': JuryFormGenerator,
    'a': ApprovalFormGenerator,
    'l': StandLabelGenerator,
    'p': PlanningGenerator,
    't': TeamsListGenerator,
    's': SignsGenerator,
    'r': RoboticsMatchFormGenerator,
    'd': DiplomasGenerator,
    'g': PostersEvalGridGenerator,
    'f': TeamRegistrationFormGenerator,
}


all_types = ''.join(sorted(_generators.keys()))


def writable_dir(value):
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
        parser.description = dedent("""
            Event forms and documents generator.

            Produces the PDF files for the various forms and documents personalized
            with the team information.

            Which documents are generated can be customized with the -g/--generate option.
            Its value is either '*' meaning 'all' or a case insensitive string of
            one letter codes representing the document types.

            Available documents are (document code given in parenthesis):
            {options}
            
            Documents depending in the results can be auto-filled with the event final results
            by using the -R/--with-results option.
        """).format(
            options='\n'.join((
                '    - ({code}) {description}'.format(code=c, description=g.description)
                for c, g in sorted(_generators.items())
            ))
        )

        parser.formatter_class = argparse.RawTextHelpFormatter

        parser.add_argument('-o', '--output_dir',
                            help='output directory, created if not found\n(default: "%(default)s")',
                            type=writable_dir,
                            default=os.path.expanduser('~/.pjc_mc/documents/'))
        parser.add_argument('-g', '--generate',
                            dest='selection',
                            help='specify which documents are to be generated\n(default: "%(default)s")',
                            type=doc_types,
                            default=all_types)
        parser.add_argument('-R', '--use-results',
                            dest='use_results',
                            help='use event results for auto-filling documents\n(default: "%(default)s")',
                            action='store_true'
                            )

    def handle(self, *args, **options):
        output_dir = options['output_dir']
        selection = options['selection']
        use_results = options['use_results']

        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        self.stdout.write('Generating documents in : %s' % output_dir)
        for generator_class in (v for k, v in _generators.items() if k in selection):
            generator = generator_class(output_dir, use_results)
            self.stdout.write('- {0:30s}'.format(generator.title), ending='')
            self.stdout.flush()

            try:
                generator.generate()

            except GenerationError as e:
                print('*** An error occurred during document generation :')
                print(' ' * 36 + str(e))
                generator.remove_report_file()

            else:
                self.stdout.write('--> %s' % os.path.basename(generator.pdf_file_path))

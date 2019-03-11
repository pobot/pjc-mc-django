# -*- coding: utf-8 -*-

from textwrap import dedent
import argparse
import os

from django.core.management import BaseCommand

__author__ = 'Eric Pascual'


class SPIPCommand(BaseCommand):
    description = ""

    def add_arguments(self, parser):
        parser.description = dedent(self.description)
        parser.formatter_class = argparse.RawTextHelpFormatter

        self.add_custom_arguments(parser)

    def add_custom_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        import pyperclip

        spip_code = self.get_spip_code()
        if isinstance(spip_code, list):
            spip_code = '\n'.join(spip_code)

        self.stdout.write("Generated code:")
        self.stdout.write(' BEGIN '.center(80, '-'))
        self.stdout.write(spip_code)
        self.stdout.write(' END '.center(80, '-'))

        try:
            pyperclip.copy(spip_code)
        except pyperclip.PyperclipException as e:
            self.stderr.write(
                "Pyperclip could not find a copy/paste mechanism for your system.\n"
                "You'll need to copy the SPIP code manually from the terminal output."
            )
        else:
            self.stdout.write("Code copied in the clipboard.")

    def get_spip_code(self):
        raise NotImplementedError()

# -*- coding: utf-8 -*-

import os
import subprocess

from django.conf import settings
from django.core.management import CommandError

from PyPDF2 import PdfFileMerger

from docmaker.commons import ReportGenerator, ASSETS_DIR

from teams.models import Team

__author__ = 'Eric Pascual'

__all__ = ['CertificateGenerator']


class CertificateGenerator(ReportGenerator):
    title = "Certificats de participation"
    output_file_name = 'certificates'
    description = "team participation certificates"
    svg_template_file = "PJC_certificat_participation.svg"

    def generate(self):
        svg_template_path = os.path.join(ASSETS_DIR, self.svg_template_file)
        if not os.path.exists(svg_template_path):
            raise CommandError('SVG template file not found at %s' % svg_template_path)

        with open(svg_template_path) as fp:
            templ = '\n'.join(fp.readlines())

        # transform the SVG XML code by something usable as a string template
        # - escape percents (used in dimensions for instance)
        # - transform our pseudo vars into format placeholders
        templ = templ.replace("%", "%%").replace("$(", "%(")

        competition_date = settings.PJC['event_date']
        edition = settings.PJC['edition']

        team_certificates = []

        tmp_svg = "/tmp/certificate.svg"
        to_be_cleaned = [tmp_svg]

        for team in Team.objects.all().order_by('num'):
            tmp_pdf_file_path = os.path.join("/tmp", "%s-%02d.pdf" % (self.output_file_name, team.num))
            with open(tmp_svg, 'w') as fp:
                fp.write(templ % {
                    'team_name': team.name,
                    'date': competition_date,
                    'edition': edition
                })
            subprocess.call("inkscape %s -A %s > /dev/null 2>&1" % (tmp_svg, tmp_pdf_file_path), shell=True)
            to_be_cleaned.append(tmp_pdf_file_path)
            team_certificates.append(tmp_pdf_file_path)

        pdf_file_name = self.output_file_name + '.pdf'
        in_files = [open(fpath, 'rb') for fpath in team_certificates]
        try:
            merger = PdfFileMerger()
            for fp in in_files:
                merger.append(fp)

            with open(os.path.join(self._output_dir, pdf_file_name), 'wb') as out_file:
                merger.write(out_file)

        finally:
            for fp in in_files:
                fp.close()

        # cleanup
        for p in to_be_cleaned:
            os.remove(p)

        return pdf_file_name

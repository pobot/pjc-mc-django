# -*- coding: utf-8 -*-

import os
import subprocess

from django.conf import settings

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
        with open(os.path.join(ASSETS_DIR, self.svg_template_file)) as fp:
            templ = '\n'.join(fp.readlines())

        # transform the SVG XML code by something usable as a string template
        # - escape percents (used in dimensions for instance)
        # - transform our pseudo vars into format placeholders
        templ = templ.replace("%", "%%").replace("$(", "%(")

        competition_date = settings.PJC['event_date']
        edition = settings.PJC['edition']

        tmp_files = []

        tmp_svg = "/tmp/certificate.svg"
        tmp_files.append(tmp_svg)

        for team in Team.objects.all():
            tmp_pdf_file_path = os.path.join("/tmp", "%s-%02d.pdf" % (self.output_file_name, team.num))
            with open(tmp_svg, 'w') as fp:
                fp.write(templ % {
                    'team_name': team.name,
                    'date': competition_date,
                    'edition': edition
                })
            subprocess.call("inkscape %s -A %s > /dev/null 2>&1" % (tmp_svg, tmp_pdf_file_path), shell=True)
            tmp_files.append(tmp_pdf_file_path)

        pdf_file_name = self.output_file_name + '.pdf'
        subprocess.call("pdftk /tmp/%s-??.pdf cat output %s" % (
            self.output_file_name, os.path.join(self._output_dir, pdf_file_name)
        ), shell=True)

        # cleanup
        for p in tmp_files:
            os.remove(p)

        return pdf_file_name

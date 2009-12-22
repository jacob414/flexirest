# -*- coding: utf-8 -*-
import os
import textwrap
import subprocess
import tempfile

from StringIO import StringIO

from nose.tools import assert_equals, assert_true, with_setup

from flexirest.tex import *
from flexirest.test import support

import support

def write_fake_style(path):
    support.write_test_file(path, textwrap.dedent(r"""
        \NeedsTeXFormat{LaTeX2e}
        \ProvidesPackage{flexifake}[2009/09/11 1.0 a test fixture used by flexirest]
        \endinput
        """))

def sanity_check_pdf(pdf):
    assert_equals(pdf[:8], '%PDF-1.4')
    assert_equals(pdf[-6:], '%%EOF\n')

def extract_pdf_text(pdf):
    return support.pdf_from_data(pdf).getPage(0).extractText()

def test_simplest():
    pdf = run_program('pdflatex', textwrap.dedent(ur"""
    \documentclass{article}
    \begin{document}
    Simplest
    \end{document}"""))
    sanity_check_pdf(pdf)
    text = extract_pdf_text(pdf)
    assert_true(text.startswith(u'Simplest'))

def test_utf8_encoded():
    # Not using raw unicode string here, see
    # http://bugs.python.org/issue1477
    # ..why does it work in the first test?
    pdf = run_program('pdflatex', textwrap.dedent(u"""
    \\documentclass{article}
    \\usepackage[utf8]{inputenc}
    \\begin{document}
    Å ä ö
    \\end{document}
    """))
    sanity_check_pdf(pdf)
    text = extract_pdf_text(pdf)
    assert_true(text.startswith(u'Aao')) # pdflatex quirkiness, but correct

_styles_dir = []

def latex_tmp(name):
    return os.path.join(_styles_dir[0], name)

def setup_styles_dir():
    _styles_dir.append(tempfile.mkdtemp(prefix='fr-test-w-style-'))
    write_fake_style(latex_tmp('flexifake.sty'))

def teardown_styles_dir():
    shutil.rmtree(_styles_dir[0])

@with_setup(setup_styles_dir, teardown_styles_dir)
def test_w_style():
    pdf = run_program('pdflatex', textwrap.dedent("""
    \\documentclass{article}
    \\usepackage{flexifake}
    \\begin{document}
    Uses package flexifake.
    \\end{document}"""), (latex_tmp('flexifake.sty'),))
    sanity_check_pdf(pdf)
    text = extract_pdf_text(pdf)
    assert_true(text.startswith(u'Usespackage'))


# -*- coding: utf-8 -*-
import os
import textwrap
import subprocess
import tempfile

from StringIO import StringIO

from nose.tools import assert_equals, assert_true, with_setup

from flexirest.tex import *

import support

def write_fake_style(path):
    support.write_test_file(path, textwrap.dedent(r"""
        \NeedsTeXFormat{LaTeX2e}
        \ProvidesPackage{flexifake}[2009/09/11 1.0 a test fixture used by flexirest]
        \endinput
        """))

def test_simplest():
    pdf = latex2pdf(textwrap.dedent(ur"""
    \documentclass{article}
    \begin{document}
    Simplest
    \end{document}"""))
    assert_equals(pdf[:8], '%PDF-1.4')
    assert_equals(pdf[-6:], '%%EOF\n')

def test_utf8_encoded():
    # Not using raw unicode string here, see
    # http://bugs.python.org/issue1477
    # ..why does it work in the first test?
    pdf = latex2pdf(textwrap.dedent(u"""
    \\documentclass{article}
    \\usepackage[utf8]{inputenc}
    \\begin{document}
    Å ä ö
    \\end{document}
    """))
    assert_equals(pdf[:8], '%PDF-1.4')
    assert_equals(pdf[-6:], '%%EOF\n')

_styles_dir = None

def setup_styles_dir():
    global _styles_dir
    _styles_dir = tempfile.mkdtemp(prefix='fr-test-w-style-')

def teardown_styles_dir():
    global _styles_dir
    shutil.rmtree(_styles_dir)

@with_setup(setup_styles_dir, teardown_styles_dir)
def test_w_style():
    global _styles_dir
    stylepath = os.path.join(_styles_dir, 'flexifake.sty')
    write_fake_style(stylepath)

    pdf = latex2pdf(textwrap.dedent("""
    \\documentclass{article}
    \\usepackage{flexifake}
    \\begin{document}
    Uses package flexifake.
    \\end{document}"""), (stylepath,))
    assert_equals(pdf[:8], '%PDF-1.4')
    assert_equals(pdf[-6:], '%%EOF\n')


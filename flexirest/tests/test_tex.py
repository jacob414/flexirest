# -*- coding: utf-8 -*-
import os
import textwrap
import subprocess
import tempfile

from StringIO import StringIO

from nose.tools import assert_equals, assert_true

from flexirest.tex import *

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

def test_w_style():
    stylesdir = tempfile.mkdtemp(prefix='fr-test-w-style-')
    stylepath = os.path.join(stylesdir, 'flexifake.sty')
    open(stylepath, 'w').write(textwrap.dedent(r"""
    \NeedsTeXFormat{LaTeX2e}
    \ProvidesPackage{flexifake}[2009/09/11 1.0 a test fixture used by flexirest]
    \endinput
    """))

    try:
        pdf = latex2pdf(textwrap.dedent("""
        \\documentclass{article}
        \\usepackage{flexifake}
        \\begin{document}
        Uses package cmap
        \\end{document}"""), (stylepath,))
        assert_equals(pdf[:8], '%PDF-1.4')
        assert_equals(pdf[-6:], '%%EOF\n')
    finally:
        shutil.rmtree(stylesdir)

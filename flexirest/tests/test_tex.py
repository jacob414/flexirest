# -*- coding: utf-8 -*-
import os
import textwrap
import subprocess

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
    pdf = latex2pdf(textwrap.dedent(u"""
    \\documentclass{article}
    \\usepackage[utf8]{inputenc}
    \\begin{document}
    Å ä ö
    \\end{document}
    """))
    assert_equals(pdf[:8], '%PDF-1.4')
    assert_equals(pdf[-6:], '%%EOF\n')

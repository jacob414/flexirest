# -*- coding: utf-8 -*-
from __future__ import with_statement

import os, sys

from functools import partial
from StringIO import StringIO

from flexirest.util import substitute

from flexirest.main import Io

__docformat__ = 'reStructuredText'

MINIMAL_FIXTURE = """
=================
A minimal fixture
=================
Text
"""

UTF8_FIXTURE = """
=====
Titel
=====

Svensk text här.
"""

get_minimal_fixture = lambda: StringIO(MINIMAL_FIXTURE)
get_utf8_fixture = lambda: StringIO(UTF8_FIXTURE)

class CapturingIo(Io):

    def __init__(self, source=None):
        super(CapturingIo, self).__init__(stderr=StringIO())
        self.destination = StringIO()
        self.console = StringIO()
        if source is None:
            self.source = get_minimal_fixture()
        else:
            self.source = source

    @property
    def message(self):
        return self.console.getvalue()

    @property
    def msglines(self):
        return self.message.split(os.linesep)

    @property
    def result(self):
        return self.destination.getvalue()

    @property
    def lines(self):
        return self.result.split(os.linesep)

    @property
    def errlines(self):
        return self.stderr.getvalue().split(os.linesep)

nullfile = partial(open, os.devnull)

class NullIo(Io):

    def __init__(self):
        super(NullIo, self).__init__(stderr=nullfile('w'))
        self.destination = nullfile('w')
        self.console = nullfile('w')

testfiles = []

def write_test_file(path, contents):
    with open(os.path.expanduser(path), 'w') as fp:
        fp.write(contents)

def create_gc_testfile(path, contents):
    write_test_file(path, contents)
    testfiles.append(path)

def clean_gc_testfiles():
    for path in testfiles:
        os.unlink(os.path.expanduser(path))
        testfiles.remove(path)

def pdf_from_file(pdf_f):
    """
    Given PDF data, returns a `pyPdf.PdfFileReader` for the
    data. Right now, `PdfFileReader` gives `DeprecationWarning`
    -messages on stderr, this functions takes care that the warnings
    are not shown (I really don't have time for a patching round right
    now).
    """
    with substitute('sys.stderr', open(os.devnull, 'w')):
        import pyPdf
        return pyPdf.PdfFileReader(pdf_f)

def pdf_from_data(pdf):
    return pdf_from_file(StringIO(pdf))

class LineCapture(object):
    """
    Used to capture output in tests. The capturer is any object that
    supports a `.write()` method (`sys.stdout` would be used in
    production code).
    """
    def __init__(self):
        self.lines = []

    def write(self, msg):
        if msg == os.linesep:
            return
        self.lines.append(msg)

    def flush(self):
        pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()

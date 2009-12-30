# -*- coding: utf-8 -*-
from __future__ import with_statement

import os
import sys
from StringIO import StringIO

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

def getraise(callable, *args, **kwargs):
    """
    Calls `callable`, expecting an exception inheriting from
    `StandardError` (your exceptions *are* inheriting from
    `StandardError`, right?), with `*args` and `**kwargs` as parameters.

    Returns the results of `sys.exc_info()` as a result.

    Isn't there something built into nose that does this? I can't find
    it.

    >>> _type, exc, tb = getraise(open, '/no/such/path')
    >>> exc
    IOError(2, 'No such file or directory')
    >>>
    """
    try:
        callable(*args, **kwargs)
    except StandardError:
        return sys.exc_info()

class Capturer(object):
    """
    Used to capture output in tests. The capturer is any object that
    supports a `.write()` method (`sys.stdout` would be used in
    production code).
    """
    def __init__(self):
        self.lines = []

    def write(self, msg):
        self.lines.append(msg)

    def flush(self):
        pass

def capture_stderr(callable, *args, **kwargs):
    """
    Calls `callable` with `*args` and `**kwargs` while capturing stderr.

    Returns `<captured stderr>, <return value of fn>`
    """
    stderr = sys.stderr
    capture = StringIO()
    try:
        sys.stderr = capture
        res = callable(*args, **kwargs)
    finally:
        sys.stderr = stderr
    return res, capture.getvalue()

testfiles = []

def write_test_file(path, contents):
    with open(path, 'w') as fp:
        fp.write(contents)

def create_gc_testfile(path, contents):
    write_test_file(path, contents)
    testfiles.append(path)

def clean_gc_testfiles():
    for path in testfiles:
        os.unlink(path)
        testfiles.remove(path)

def pdf_from_file(pdf_f):
    """
    Given PDF data, returns a `pyPdf.PdfFileReader` for the
    data. Right now, `PdfFileReader` gives `DeprecationWarning`
    -messages on stderr, this functions takes care that the warnings
    are not shown (I really don't have time for a patching round right
    now).
    """

    stderr = sys.stderr
    try:
        sys.stderr = open(os.devnull, 'w')
        import pyPdf
        pdf_o = pyPdf.PdfFileReader(pdf_f)
    finally:
        sys.stderr = stderr

    return pdf_o

def pdf_from_data(pdf):
    return pdf_from_file(StringIO(pdf))

if __name__ == '__main__':
    import doctest
    doctest.testmod()

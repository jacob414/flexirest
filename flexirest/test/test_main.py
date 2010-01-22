from __future__ import with_statement

import os
import sys
import imp
import errno

from StringIO import StringIO

from nose.tools import assert_equals, assert_true, with_setup, raises

from aspektratio.util import substitute
from aspektratio.testing import LineCapture

from flexirest import main, meta, rendering
from flexirest.test import support

def test_info():
    out = StringIO()
    rc = main.commandline_new(args=(), console=out)
    assert_equals(rc, 0)
    assert_true(out.getvalue().startswith('Flexirest'))

def test_version():
    outp = LineCapture()
    retc = main.commandline_new(args=['version',], console=outp)
    assert_equals(retc, 0)
    assert_equals(outp.lines, [meta.VERSION])

def test_show_status():
    out = LineCapture()
    rc = main.commandline_new(args=['status'], console=out)

def test_list_writers():
    outp = LineCapture()
    retc = main.commandline(args=['--list-writers',], console=outp)
    assert_equals(retc, 0)
    # XXX Sanity check only for now
    for expected in ('html', 'latex', 'latex2e'):
        yield assert_true, lambda: expected in outp.lines

def test_dump_parts():
    capture = LineCapture()
    rc = main.commandline(['--dump-parts', '--writer=latex'],
                          source=support.get_minimal_fixture(),
                          destination=capture)
    # XXX Sanity check only
    assert_true(capture.lines[0].startswith("Parts created by the docutils"))

@raises(ImportError)
def test_explicit_confmodule_not_found_raises():
    #import ipdb; ipdb.set_trace()
    main.commandline(['--config=notamodule'])

def test_no_default_confmodule_noraise():
    main.commandline([], source=support.get_minimal_fixture())

def test_bad_writer_nice_error():
    capture = LineCapture()
    with substitute('sys.stderr', capture):
        rval = main.commandline(['--writer=bad_writer'])
    assert_equals(rval, errno.EINVAL)
    assert_equals(capture.lines,
                  ["flexirest: 'bad_writer' is not a valid writer%s" % os.linesep])


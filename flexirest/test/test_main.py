from __future__ import with_statement

import os, sys, imp, errno

from StringIO import StringIO

from nose.tools import assert_equals, assert_true, with_setup, raises

from aspektratio.util import substitute
from aspektratio.testing import LineCapture

from flexirest import main, meta, rendering
from flexirest.test import support

def test_info():
    """
    Tests output of running without parameters
    """
    io = support.CapturingIO()
    rc = main.commandline_new(args=(), io=io)
    assert_equals(rc, 0)
    assert_true(io.message.startswith('Flexirest'))

def test_version():
    """
    Tests the output of the 'version' command
    """
    def check_version(variant):
        io = support.CapturingIO()
        retc = main.commandline_new(args=[variant,], io=io)
        assert_equals(retc, 0)
        assert_equals(io.msglines, [meta.VERSION, ''])

    for variant in ('-v', '--version', 'version'):
        yield check_version, variant

expected_status_start = (
"""The following writers are functional in your installation:
    html          HTML (docutils builtin)
    latex         LaTeX (docutils built in)""")

def test_show_status():
    """
    Tests the output of the 'status' command
    """
    def check_status(variant):
        io = support.CapturingIO()
        rc = main.commandline_new(args=[variant], io=io)
        assert_equals(rc, 0)
        assert_true(io.message.startswith(expected_status_start))

    for variant in ('status', 'st'):
        yield check_status, variant

def test_dump_parts():
    io = support.CapturingIO()
    io.source = support.get_minimal_fixture()
    rc = main.commandline_new(['latex', '--dump-parts'], io=io)
    # XXX sanity check only
    assert_true(io.lines[0].startswith("Parts created by the docutils"))

@raises(ImportError)
def test_explicit_confmodule_not_found_raises():
    main.commandline_new(['latex', '--config=notamodule'])

def test_no_default_confmodule_noraise():
    main.commandline_new([], source=support.get_minimal_fixture())

def test_bad_writer_nice_error():
    capture = LineCapture()
    with substitute('sys.stderr', capture):
        rval = main.commandline(['--writer=bad_writer'])
    assert_equals(rval, errno.EINVAL)
    assert_equals(capture.lines,
                  ["flexirest: 'bad_writer' is not a valid writer%s" % os.linesep])


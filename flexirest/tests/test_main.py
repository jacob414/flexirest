import os
import sys
import imp

from StringIO import StringIO

from flexirest import main, meta, rendering
from nose.tools import assert_equals, assert_true, with_setup, raises

from flexirest.tests.support import Capturer, get_minimal_fixture

def test_help():
    outp = Capturer()
    old_stdout = sys.stdout
    try:
        sys.stdout = outp
        retc = main.commandline(args=['--help'])
    except SystemExit, e:
        assert_equals(e.code, 0)
    finally:
        sys.stdout = old_stdout
        _help = outp.lines[0].split(os.linesep)
        assert_equals(_help[0], 'Usage: flexirest <options>')
        assert_true(_help[5].endswith('show this help message and exit'))

def test_version():
    outp = Capturer()
    retc = main.commandline(args=['--version',], console=outp)
    assert_equals(retc, 0)
    assert_equals(outp.lines, ["flexirest version %s" % meta.VERSION])

def test_list_writers():
    outp = Capturer()
    retc = main.commandline(args=['--list-writers',], console=outp)
    assert_equals(retc, 0)
    # XXX Sanity check only for now
    for expected in ('html', 'latex', 'latex2e'):
        yield assert_true, lambda: expected in outp.lines

def test_dump_parts():
    capture = Capturer()
    rc = main.commandline(['--dump-parts', '--writer=latex'],
                          source=get_minimal_fixture(),
                          destination=capture)
    # XXX Sanity check only
    assert_true(capture.lines[0].startswith("Parts created by the docutils"))

@raises(ImportError)
def test_explicit_confmodule_not_found_raises():
    main.commandline(['--config=notamodule'])

def test_no_default_confmodule_noraise():
    main.commandline([], source=get_minimal_fixture())

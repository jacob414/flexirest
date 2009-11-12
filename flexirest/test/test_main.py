import os
import sys
import imp
import errno

from StringIO import StringIO

from flexirest import main, meta, rendering
from nose.tools import assert_equals, assert_true, with_setup, raises

from flexirest.test import support

def test_help():
    outp = support.Capturer()
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
    outp = support.Capturer()
    retc = main.commandline(args=['--version',], console=outp)
    assert_equals(retc, 0)
    assert_equals(outp.lines, ["flexirest version %s" % meta.VERSION])

def test_list_writers():
    outp = support.Capturer()
    retc = main.commandline(args=['--list-writers',], console=outp)
    assert_equals(retc, 0)
    # XXX Sanity check only for now
    for expected in ('html', 'latex', 'latex2e'):
        yield assert_true, lambda: expected in outp.lines

def test_dump_parts():
    capture = support.Capturer()
    rc = main.commandline(['--dump-parts', '--writer=latex'],
                          source=support.get_minimal_fixture(),
                          destination=capture)
    # XXX Sanity check only
    assert_true(capture.lines[0].startswith("Parts created by the docutils"))

@raises(ImportError)
def test_explicit_confmodule_not_found_raises():
    main.commandline(['--config=notamodule'])

def test_no_default_confmodule_noraise():
    main.commandline([], source=support.get_minimal_fixture())

def test_bad_writer_nice_error():
    rval, stderr = support.capture_stderr(main.commandline,
                                          ['--writer=bad_writer'])
    assert_equals(rval, errno.EINVAL)
    assert_equals(stderr, "flexirest: 'bad_writer' is not a valid writer%s" % os.linesep)


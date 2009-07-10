import os
import sys

from flexirest import main, meta
from nose.tools import assert_equals, assert_true

from flexirest.tests.support import Capturer

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
        assert_true(_help[-2].endswith('-v, --version  print version and exit'))

def test_version():
    outp = Capturer()
    retc = main.commandline(args=['--version',], console=outp)
    assert_equals(retc, 0)
    assert_equals(outp.lines, ["flexirest version '%s'" % meta.VERSION])

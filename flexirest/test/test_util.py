import os
import shutil

from StringIO import StringIO

from nose.tools import assert_equals, assert_true, assert_false, with_setup

from flexirest import util

def test_StdoutConsoleWrite():
    sc = util.StdoutConsole()
    sc.out = StringIO()
    sc.write('hello!')
    assert_equals(sc.out.getvalue(), 'hello!' + os.linesep)

def test_Duck():
    d = util.Duck(ze_attr='ze attr')
    assert_equals(d.ze_attr, 'ze attr')

def test_has_program_ok():
    # XXX Posix centric, won't work on windows... find known good program
    assert_true(util.has_program('ls'))

def test_has_program_ok_w_options():
    # XXX see XXX in test_has_program_ok()
    assert_true(util.has_program('ls', '-l'))

def test_has_program_no_exist():
    assert_false(util.has_program('this-is-cleary-bogus'))

import os

from StringIO import StringIO

from nose.tools import assert_equals

from flexirest import util

def test_StdoutConsoleWrite():
    sc = util.StdoutConsole()
    sc.out = StringIO()
    sc.write('hello!')
    assert_equals(sc.out.getvalue(), 'hello!' + os.linesep)

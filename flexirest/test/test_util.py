import os

from StringIO import StringIO

from nose.tools import assert_equals, assert_false, with_setup

from flexirest import util

def test_StdoutConsoleWrite():
    sc = util.StdoutConsole()
    sc.out = StringIO()
    sc.write('hello!')
    assert_equals(sc.out.getvalue(), 'hello!' + os.linesep)

def test_Duck():
    d = util.Duck(ze_attr='ze attr')
    assert_equals(d.ze_attr, 'ze attr')


class TestBufferedFile(object):

    # XXX Implementation drawback: platform dependant
    @with_setup(lambda: None, lambda: os.unlink('/tmp/write.this'))
    def test_write(self):
        bf = util.BufferedFile('/tmp/write.this')
        bf.write('what was written')
        bf.close()
        assert_equals(open('/tmp/write.this', 'r').read(), 'what was written')

    # XXX Implementation drawback: platform dependant
    def test_no_write(self):
        bf = util.BufferedFile('/tmp/dont.write.this')
        bf.close()
        assert_false(os.path.exists('/tmp/dont.write.this'))

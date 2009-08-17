import textwrap
import functools
import imp

from nose.tools import assert_equals, assert_true, with_setup, raises

from .. import support

from flexirest import main

from StringIO import StringIO

MINIMAL_FIXTURE = StringIO("""
======
654321
======
RST Text
""")

BASIC_TMPL = '/tmp/tmpl_basic.txt'

test_tmpl_1_creator = functools.partial(support.create_testfile, BASIC_TMPL, textwrap.dedent("""
the_template %(whole)s
"""))

@with_setup(test_tmpl_1_creator, support.clean_testfiles)
def test_template_basic():
    capture = StringIO()
    main._import = imp.new_module
    rc = main.commandline(['--template=%s' % BASIC_TMPL, '--writer=pseudoxml'],
                          source=MINIMAL_FIXTURE, destination=capture)
    out = capture.getvalue()
    assert_true('the_template' in out)
    assert_true('title="654321"' in out)

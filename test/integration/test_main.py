import textwrap
import functools
import imp

from nose.tools import assert_equals, assert_true, with_setup, raises

from .. import support

from flexirest import main

from StringIO import StringIO

MINIMAL_FIXTURE = StringIO("""
=====
Title
=====
Text
""")

BASIC_TMPL = '/tmp/tmpl_basic.txt'

test_tmpl_1_creator = functools.partial(support.create_testfile, BASIC_TMPL, textwrap.dedent("""

"""))

@with_setup(test_tmpl_1_creator, support.clean_testfiles)
def test_template_basic():
    main._import = imp.new_module
    rc = main.commandline(['--template', BASIC_TMPL, '--writer', 'latex2e'],
                          source=MINIMAL_FIXTURE)

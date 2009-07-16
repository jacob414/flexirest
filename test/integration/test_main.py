import textwrap

from nose.tools import assert_equals, assert_true, with_setup, raises

from .. import support

def test_template_basic():
    support.create_testfile('/tmp/tmpl_basic.txt', textwrap.dedent("""


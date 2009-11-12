import sys
import doctest
from flexirest.test import support

from nose.tools import assert_equals

def test_capture_stderr():
    assert_equals(support.capture_stderr(lambda: sys.stderr.write('captured!')),
                  (None, 'captured!'))

def test_run_support_doctests():
    doctest.testmod(support)

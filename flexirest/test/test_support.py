import sys
import doctest
from flexirest.test import support

from nose.tools import assert_equals

def test_run_support_doctests():
    doctest.testmod(support)

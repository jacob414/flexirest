import sys
import doctest
from flexirest.test import support

def test_run_support_doctests():
    doctest.testmod(support)

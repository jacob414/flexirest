import doctest
from flexirest.tests import support

def test_run_support_doctests():
    doctest.testmod(support)

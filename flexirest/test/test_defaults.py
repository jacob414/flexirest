from flexirest.defaults import templates

from nose.tools import assert_true

def test_nonstandard_defaults():
    assert_true(templates['html'] != u'%(whole)s')

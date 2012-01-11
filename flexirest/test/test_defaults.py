from flexirest.defaults import templates

def test_nonstandard_defaults():
    assert templates['html'] != u'%(whole)s'

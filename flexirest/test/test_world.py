from nose.tools import assert_true

from flexirest import world

def test_all_strategies():
    # Sanity test with a few known writer names
    assert_true(
        set(('html', 'latex', 'latex',)).issubset(world.all_strategies))

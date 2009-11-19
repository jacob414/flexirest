import imp
from StringIO import StringIO

from flexirest import rendering, defaults, util
from flexirest.test import support

from nose.tools import assert_equals, assert_true, with_setup, raises

roles_registered = set()

old_regrole = rendering.roles.register_canonical_role

def role_one():
    pass

def role_two():
    pass

def patched_register_canonical_role(name, func):
    print( 'REG ROLE ', name)
    roles_registered.add(name)

def monkeypatch_regrole():
    old_regrole = rendering.roles.register_canonical_role
    rendering.roles.register_canonical_role = patched_register_canonical_role

def unpatch_regrole():
    rendering.roles.register_canonical_role = old_regrole

@with_setup(monkeypatch_regrole, unpatch_regrole)
def test_roles():
    confmod = imp.new_module('flexiconf')

    def role_one(): pass
    def role_two(): pass
    class empty_callable(object):
        def __call__(self): pass
    i_am_callable = empty_callable()

    confmod.role_one = role_one
    confmod.role_two = role_two
    confmod.role_three = i_am_callable
    confmod.role_four = "but I'm not callable!"

    out = StringIO()
    rendering.render(support.get_minimal_fixture(),
                     out,
                     confmod,
                     util.Duck(lang='en', dump_parts=False),
                     defaults.templates['html'], 'html')

    assert_true(set(('one', 'two', 'three')).issubset(roles_registered))


def test_dump_parts():
    out = support.Capturer()
    rendering.dump_parts(support.get_minimal_fixture(),
                         out,
                         imp.new_module('flexiconf'),
                         util.Duck(lang='en', dump_parts=True),
                         defaults.templates['html'], 'html')
    assert_true(out.lines[0].startswith("Parts created by the docutils writer 'html'"))
    assert_true(out.lines[4].startswith('body'))

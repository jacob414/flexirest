import imp
from StringIO import StringIO

from nose.tools import assert_equals, assert_true, with_setup, raises

from aspektratio.testing import LineCapture

from flexirest import rendering, strategies, defaults, util
from flexirest.test import support

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

    rendering.render(strategies.HtmlStrategy(),
                     support.CapturingIo(),
                     confmod,
                     util.Duck(lang='en', dump_parts=False),
                     defaults.templates['html'])

    assert_true(set(('one', 'two', 'three')).issubset(roles_registered))


def test_dump_parts():
    io = support.CapturingIo()
    rendering.dump_parts(strategies.HtmlStrategy(),
                         io,
                         imp.new_module('flexiconf'),
                         util.Duck(lang='en', dump_parts=True),
                         defaults.templates['html'])
    assert_true(io.msglines[0].startswith("Parts created by the docutils writer 'html4css1'"))
    assert_true(io.msglines[9].startswith('body'))

def test_dump_parts_utf8():
    out = LineCapture()
    io = support.CapturingIo()
    rendering.dump_parts(strategies.LatexStrategy(),
                         io,
                         imp.new_module('flexiconf'),
                         util.Duck(lang='sv', dump_parts=True, resources=False),
                         defaults.templates['latex'])
    assert_true(io.msglines[0].startswith("Parts created by the docutils writer 'latex2e'"))
    assert_true(io.msglines[9].startswith('abstract'))

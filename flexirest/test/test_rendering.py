import imp
from StringIO import StringIO


from flexirest import rendering, strategies, defaults, util
from flexirest.test import support
from flexirest.test.support import LineCapture

roles_registered = set()

old_regrole = rendering.roles.register_canonical_role

def role_one():
    pass

def role_two():
    pass

def patched_register_canonical_role(name, func):
    print( 'REG ROLE ', name)
    roles_registered.add(name)

def test_roles():
    try:
        old_regrole = rendering.roles.register_canonical_role
        rendering.roles.register_canonical_role = patched_register_canonical_role
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

        assert set(('one', 'two', 'three')).issubset(roles_registered)
    finally:
        rendering.roles.register_canonical_role = old_regrole

def test_dump_parts():
    io = support.CapturingIo()
    rendering.dump_parts(strategies.HtmlStrategy(),
                         io,
                         imp.new_module('flexiconf'),
                         util.Duck(lang='en', dump_parts=True),
                         defaults.templates['html'])
    assert io.msglines[0].startswith(
        "Parts created by the docutils writer 'html4css1'")
    assert io.msglines[9].startswith('body')

def test_dump_parts_utf8():
    out = LineCapture()
    io = support.CapturingIo()
    rendering.dump_parts(strategies.LatexStrategy(),
                         io,
                         imp.new_module('flexiconf'),
                         util.Duck(lang='sv', dump_parts=True, resources=False),
                         defaults.templates['latex'])
    assert io.msglines[0].startswith("Parts created by the docutils writer 'latex2e'")
    assert io.msglines[9].startswith('abstract')

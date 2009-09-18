import textwrap
import functools
import imp

from docutils import nodes

from nose.tools import assert_equals, assert_true, with_setup, raises

from .. import support

from flexirest import main

from StringIO import StringIO

MINIMAL_FIXTURE = StringIO("""
======
654321
======
RST Text
""")

BASIC_TMPL = '/tmp/tmpl_basic.txt'

test_tmpl_basic_creator = functools.partial(support.create_testfile, BASIC_TMPL, textwrap.dedent("""
the_template %(whole)s
"""))

@with_setup(test_tmpl_basic_creator, support.clean_testfiles)
def test_template_basic():
    capture = StringIO()
    main._import = imp.new_module
    rc = main.commandline(['--template=%s' % BASIC_TMPL, '--writer=pseudoxml'],
                          source=MINIMAL_FIXTURE, destination=capture)
    out = capture.getvalue()
    assert_true('the_template' in out)
    assert_true('title="654321"' in out)

def role_foo(role, rawtext, text, lineno, inliner, options=None, content=[]):
    if options is None:
        options = {}
    node = nodes.TextElement(text=u'ROLESTART_%s_ROLESTOP' % text)
    return node, []

ROLE_TMPL = '/tmp/tmpl_full_role.txt'

test_tmpl_full_role_creator = functools.partial(support.create_testfile,
                                                ROLE_TMPL,
                                                textwrap.dedent("""
the_template %(whole)s
"""))

@with_setup(test_tmpl_full_role_creator, support.clean_testfiles)
def test_full_role():
    fullrole_src = StringIO(textwrap.dedent("""
    Some text :foo:`Some test text` after
    """))

    rolesmod = imp.new_module('roles')
    rolesmod.role_foo = role_foo
    main._import = lambda n: rolesmod
    capture = StringIO()
    rc = main.commandline(['--template=%s' % ROLE_TMPL, '--writer=pseudoxml'],
                          source=fullrole_src, destination=capture)
    out = capture.getvalue()
    assert_true('ROLESTART_Some test text_ROLESTOP' in out)

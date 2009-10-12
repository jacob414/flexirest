import os
import textwrap
import functools
import imp

from docutils import nodes

from nose.tools import assert_equals, assert_true, with_setup, raises

import support

from flexirest import main

from StringIO import StringIO

def get_minimal_fixture():
    return StringIO(textwrap.dedent("""
                                    ======
                                    654321
                                    ======
                                    RST Text
                                    """))

BASIC_TMPL = '/tmp/tmpl_basic.txt'

tmpl_basic_creator = functools.partial(support.create_testfile, BASIC_TMPL, textwrap.dedent("""
the_template %(whole)s
"""))

@with_setup(tmpl_basic_creator, support.clean_testfiles)
def test_template_basic():
    capture = StringIO()
    main._import = lambda m, r: imp.new_module(m)
    rc = main.commandline(['--template=%s' % BASIC_TMPL, '--writer=pseudoxml'],
                          source=get_minimal_fixture(), destination=capture)
    out = capture.getvalue()
    assert_true('the_template' in out)
    assert_true('title="654321"' in out)

def role_foo(role, rawtext, text, lineno, inliner, options=None, content=[]):
    if options is None:
        options = {}
    node = nodes.TextElement(text=u'ROLESTART_%s_ROLESTOP' % text)
    return node, []

ROLE_TMPL = '/tmp/tmpl_full_role.txt'

tmpl_full_role_creator = functools.partial(support.create_testfile,
                                                ROLE_TMPL,
                                                textwrap.dedent("""
the_template %(whole)s
"""))

@with_setup(tmpl_full_role_creator, support.clean_testfiles)
def test_full_role():
    fullrole_src = StringIO(textwrap.dedent("""
    Some text :foo:`Some test text` after
    """))

    rolesmod = imp.new_module('roles')
    rolesmod.role_foo = role_foo
    main._import = lambda m, r: rolesmod
    capture = StringIO()
    rc = main.commandline(['--template=%s' % ROLE_TMPL, '--writer=pseudoxml'],
                          source=fullrole_src, destination=capture)
    out = capture.getvalue()
    assert_true('ROLESTART_Some test text_ROLESTOP' in out)

SIMPLE_INFILE_PATH = '/tmp/simple_infile.rst'

simple_infile_creator = functools.partial(support.create_testfile,
                                          SIMPLE_INFILE_PATH,
                                          get_minimal_fixture().getvalue())

@with_setup(simple_infile_creator, support.clean_testfiles)
def test_w_infile():
    capture = StringIO()
    rc = main.commandline(['--infile=%s' % SIMPLE_INFILE_PATH, '--writer=html'],
                          destination=capture)
    assert_equals(rc, 0)
    assert_true('<title>654321</title>' in capture.getvalue())

SIMPLE_OUTFILE = '/tmp/simple_outfile.html'

@with_setup(lambda: None, functools.partial(os.unlink, SIMPLE_OUTFILE))
def test_w_outfile():
    rc = main.commandline(['--outfile=%s' % SIMPLE_OUTFILE, '--writer=html'],
                          source=get_minimal_fixture())
    assert_equals(rc, 0)
    assert_true('<title>654321</title>' in open(SIMPLE_OUTFILE, 'r').read())

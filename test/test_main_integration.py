import os
import textwrap
import functools
import imp
import shutil
import tempfile

from docutils import nodes

from nose.tools import assert_equals, assert_true, with_setup, raises

from flexirest.tests import support

from flexirest import main
from flexirest.tests import test_tex

from StringIO import StringIO

# XXX Use support.get_minimal_fixture instead!
def get_minimal_fixture():
    return StringIO(textwrap.dedent("""
                                    ======
                                    654321
                                    ======
                                    RST Text
                                    """))

BASIC_TMPL = '/tmp/tmpl_basic.txt'

tmpl_basic_creator = functools.partial(support.create_gc_testfile, BASIC_TMPL, textwrap.dedent("""
the_template %(whole)s
"""))

@with_setup(tmpl_basic_creator, support.clean_gc_testfiles)
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

tmpl_full_role_creator = functools.partial(support.create_gc_testfile,
                                                ROLE_TMPL,
                                                textwrap.dedent("""
the_template %(whole)s
"""))

@with_setup(tmpl_full_role_creator, support.clean_gc_testfiles)
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

simple_infile_creator = functools.partial(support.create_gc_testfile,
                                          SIMPLE_INFILE_PATH,
                                          get_minimal_fixture().getvalue())

@with_setup(simple_infile_creator, support.clean_gc_testfiles)
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

full_latex_dir = []

def setup_latex_dir():
    full_latex_dir.append(tempfile.mkdtemp(prefix='fr-latex2pdf-smoketest-'))

def teardown_latex_dir():
    shutil.rmtree(full_latex_dir[0])

def latex_tmp(name):
    return os.path.join(full_latex_dir[0], name)

@with_setup(setup_latex_dir, teardown_latex_dir)
def test_smoketest_latex2pdf_writing():
    rst_path = latex_tmp('rst-source.rst')
    support.write_test_file(rst_path, support.MINIMAL_FIXTURE)
    test_tex.write_fake_style(latex_tmp('flexifake.sty'))
    # XXX: Todo, create a template that demands the style file.

    capture = StringIO()
    rc = main.commandline(['--infile=%s' % rst_path, '--writer=latex2pdf'],
                          destination=capture)
    assert_equals(rc, 0)
    pdf = capture.getvalue()
    assert_equals(pdf[:8], '%PDF-1.4')
    assert_equals(pdf[-6:], '%%EOF\n')

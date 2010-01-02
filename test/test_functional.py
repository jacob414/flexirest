# -*- coding: utf-8 -*-
import os
import textwrap
import imp
import shutil
import tempfile

from functools import partial

from docutils import nodes

from nose.tools import (assert_equals, assert_true, assert_false,
                        with_setup, raises)
from nose.plugins.skip import SkipTest

from flexirest import main, util
from flexirest.test import support, test_tex

from StringIO import StringIO

BASIC_TMPL = '/tmp/tmpl_basic.txt'

tmpl_basic_creator = partial(support.create_gc_testfile, BASIC_TMPL, textwrap.dedent("""
the_template %(whole)s
"""))

@with_setup(tmpl_basic_creator, support.clean_gc_testfiles)
def test_template_basic():
    """
    Make a minimal template and see that `docutils` content gets
    correctly applied to it.
    """
    capture = StringIO()
    main._import = lambda m, r: imp.new_module(m)
    rc = main.commandline(['--template=%s' % BASIC_TMPL, '--writer=pseudoxml'],
                          source=support.get_minimal_fixture(),
                          destination=capture)
    out = capture.getvalue()
    assert_true('the_template' in out)
    assert_true('title="A minimal fixture"' in out)

def role_foo(role, rawtext, text, lineno, inliner, options=None, content=[]):
    """
    A minimal `docutils` role.
    """
    if options is None:
        options = {}
    node = nodes.TextElement(text=u'ROLESTART_%s_ROLESTOP' % text)
    return node, []

ROLE_TMPL = '/tmp/tmpl_full_role.txt'

tmpl_full_role_creator = partial(support.create_gc_testfile,
                                                ROLE_TMPL,
                                                textwrap.dedent("""
the_template %(whole)s
"""))

@with_setup(tmpl_full_role_creator, support.clean_gc_testfiles)
def test_full_role():
    """
    Try out a role that actually does something.
    """
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

simple_infile_creator = partial(support.create_gc_testfile,
                                          SIMPLE_INFILE_PATH,
                                          support.MINIMAL_FIXTURE)

@with_setup(simple_infile_creator, support.clean_gc_testfiles)
def test_w_infile():
    """
    Tests the `--infile` commandline option.
    """
    capture = StringIO()
    rc = main.commandline(['--infile=%s' % SIMPLE_INFILE_PATH, '--writer=html'],
                          destination=capture)
    assert_equals(rc, 0)
    assert_true('<title>A minimal fixture</title>' in capture.getvalue())

SIMPLE_OUTFILE = '/tmp/simple_outfile.html'

@with_setup(lambda: None, partial(os.unlink, SIMPLE_OUTFILE))
def test_w_outfile():
    """
    Tests the `--outfile` commandline option.
    """
    rc = main.commandline(['--outfile=%s' % SIMPLE_OUTFILE, '--writer=html'],
                          source=support.get_minimal_fixture())
    assert_equals(rc, 0)
    assert_true('<title>A minimal fixture</title>' in open(SIMPLE_OUTFILE, 'r').read())

def test_no_empty_outfile():
    """
    Tests that empty outfiles are not created after runs with errors.
    """
    try:
        support.capture_stderr(main.commandline, ['--writer=bad', '--outfile=out.file'])
        assert_true(False)
    except:
        assert_false(os.path.exists('out.file'))

full_latex_dir = []
latex_tmp = lambda n: full_latex_dir[0].newpath(n)

def setup_latex_dir(prefix):
    """
    Creates and populates the temporary directory to run `pdflatex` in.
    """
    td = util.TempDirectory(prefix)
    td.manifest()
    test_tex.write_fake_style(td.newpath('flexistyle.sty'))
    td.put('template.tex', '%(whole)s')
    full_latex_dir.append(td)

def teardown_latex_dir():
    """
    Cleans up after a LaTeX run.
    """
    full_latex_dir.pop().cleanup()

latex2pdf_setup = partial(setup_latex_dir, 'fr-latex2pdf-full-')

@with_setup(latex2pdf_setup, teardown_latex_dir)
def test_full_latex2pdf_writing():
    """
    Full run of the `latex2pdf` pseudo-writer.
    """
    capture = StringIO()
    rc, stderr = support.capture_stderr(
        main.commandline,
        ['--writer=latex2pdf',
         '--lang=sv',
         '--template=%s' % latex_tmp('template.tex')],
        source=support.get_utf8_fixture(),
        destination=capture )
    if rc == os.errno.EINVAL:
         # This means `pdflatex` wasn't available on this system. It's not an
         # error condition.
        raise SkipTest
    assert_equals(rc, 0)
    pdf = support.pdf_from_file(capture)
    assert_equals(pdf.documentInfo.title, 'Titel')
    assert_true(pdf.getPage(0).extractText().startswith(u'TitelSvensktexthär.'))

xelatex_setup = partial(setup_latex_dir, 'fr-xelatex-full-')

@with_setup(xelatex_setup, teardown_latex_dir)
def test_full_xelatex_writing():
    """
    Full run of the `xelatex` (XeLaTeX) pseudo-writer.
    """
    capture = StringIO()
    rc, stderr = support.capture_stderr(
        main.commandline,
        ['--writer=xelatex',
         '--lang=sv',
         '--template=%s' % latex_tmp('template.tex')],
        source=support.get_utf8_fixture(),
        destination=capture )
    if rc == os.errno.EINVAL:
        # This means `xelatex` wasn't available on this system. It's not an
        # error condition.
        raise SkipTest("Can't locate `xelatex`")

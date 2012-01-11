# -*- coding: utf-8 -*-
import os
import textwrap
import imp
import shutil
import tempfile
import errno

from functools import partial

from docutils import nodes

from flexirest.io import TempDirectory

from flexirest import main, util
from flexirest.test import support, test_tex
from flexirest.test.support import substitute

from StringIO import StringIO

BASIC_TMPL = '/tmp/tmpl_basic.txt'

tmpl_basic_creator = partial(support.create_gc_testfile, BASIC_TMPL, textwrap.dedent("""
the_template %(whole)s
"""))

def test_template_basic():
    """
    Make a minimal template and see that `docutils` content gets
    correctly applied to it.
    """
    try:
        tmpl_basic_creator()
        io = support.CapturingIo()
        main._import = lambda m, r: imp.new_module(m)
        rc = main.commandline(['pseudoxml', '--template=%s' % BASIC_TMPL],
                              io=io)
        assert 'the_template' in io.result
        assert 'title="A minimal fixture"' in io.result
    finally:
        supp.clean_gc_testfiles()

TMPL_IN_HOME = '~/tmpl_in_home.txt'

tmpl_in_home_creator = partial(support.create_gc_testfile, TMPL_IN_HOME,
                               '%(whole)s')

def test_template_in_home():
    """
    Tests that templates in the users home directories are correctly
    opened.
    """
    try:
        tmpl_in_home_creator()
        io = support.CapturingIo()
        rc = main.commandline(['html', '--template=%s' % TMPL_IN_HOME],
                              io=io)
        assert 0 == rc
    finally:
        support.clean_gc_testfiles()

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

def test_full_role():
    """
    Try out a role that actually does something.
    """
    try:
        tmpl_full_role_creator()
        io = support.CapturingIo(
            source = StringIO(textwrap.dedent("""
            Some text :foo:`Some test text` after
            """))
            )

        rolesmod = imp.new_module('roles')
        rolesmod.role_foo = role_foo
        main._import = lambda m, r: rolesmod
        rc = main.commandline(['pseudoxml',
                               '--template=%s' % ROLE_TMPL],
                              io=io)
        assert_true('ROLESTART_Some test text_ROLESTOP' in io.result)
    finally:
        support.clean_gc_testfiles()

SIMPLE_INFILE_PATH = '/tmp/simple_infile.rst'

simple_infile_creator = partial(support.create_gc_testfile,
                                SIMPLE_INFILE_PATH,
                                support.MINIMAL_FIXTURE)

def test_w_infile():
    """
    Tests using a named infile.
    """
    try:
        simple_infile_creator()
        io = support.CapturingIo()
        rc = main.commandline(['html', SIMPLE_INFILE_PATH], io)
        assert rc == 0
        assert '<title>A minimal fixture</title>' in io.result
    finally:
        support.clean_gc_testfiles()

INFILE_IN_HOME = '~/infile_inhome.rst'

infile_in_home = partial(support.create_gc_testfile,
                         INFILE_IN_HOME,
                         support.MINIMAL_FIXTURE)

def test_infile_in_home():
    """
    Enshures that the `--infile` option property expands home
    directories (`~`).
    """
    try:
        infile_in_home()
        io = support.CapturingIo()
        rc = main.commandline(['html', INFILE_IN_HOME], io)
        assert rc == 0
    finally:
        support.clean_gc_testfiles()

SIMPLE_OUTFILE = '/tmp/simple_outfile.html'

def test_w_outfile():
    """
    Tests the `--outfile` commandline option.
    """
    try:
        io = support.CapturingIo()
        rc = main.commandline(['html', '--outfile=%s' % SIMPLE_OUTFILE],
                              io=support.CapturingIo())
        assert_equals(rc, 0)
        assert_true('<title>A minimal fixture</title>'
                    in open(SIMPLE_OUTFILE, 'r').read())
    finally:
        os.unlink(SIMPLE_OUTFILE)

def test_infile_and_outfile():
    """
    Tests the <infile> <outfile> syntax.
    """
    with TempDirectory('fr-in-out') as td:
        td.put('infile.rst', support.MINIMAL_FIXTURE)
        rc = main.commandline(['html', td.newpath('infile.rst'),
                               td.newpath('outfile.html')],
                              io=support.NullIo())
        assert rc == 0
        assert ('<title>A minimal fixture</title>'
                    in td.open('outfile.html', 'r').read() )

def test_no_empty_outfile():
    """
    Tests that empty outfiles are not created after runs with errors.
    """
    try:
        support.capture_stderr(main.commandline, ['bad-writer', '--outfile=out.file'])
        assert_true(False)
    except:
        assert_false(os.path.exists('out.file'))

full_latex_dir = []
latex_tmp = lambda n: full_latex_dir[0].newpath(n)

def setup_latex_dir(prefix):
    """
    Creates and populates the temporary directory to run `pdflatex` in.
    """
    td = TempDirectory(prefix)
    td.manifest()
    test_tex.write_fake_style(td.newpath('flexistyle.sty'))
    td.put('template.tex', '{{whole}}')
    full_latex_dir.append(td)

def teardown_latex_dir():
    """
    Cleans up after a LaTeX run.
    """
    full_latex_dir.pop().cleanup()

latex2pdf_setup = partial(setup_latex_dir, 'fr-latex2pdf-full-')

def check_pdf_result(rc, io):
    """
    Sanity checks on results of `pdflatex` and `xelatex` runs.
    """
    assert_equals(rc, 0)
    pdf = support.pdf_from_file(io.destination)
    assert_equals(pdf.documentInfo.title, 'Titel')
    assert_true(pdf.getPage(0).extractText().startswith(u'TitelSvensktexthär.'))

def test_full_latex2pdf_writing():
    """
    Full run of the `latex2pdf` pseudo-writer.
    """
    try:
        latex2pdf_setup()
        io = support.CapturingIo()
        io.source = support.get_utf8_fixture()
        rc = main.commandline(['pdflatex',
                               '--lang=sv',
                               '--template=%s' % latex_tmp('template.tex')],
                              io=io)
        if rc == errno.ENOSYS:
            pytest.skip('pdflatex not present on system')

        check_pdf_result(rc, io)
    finally:
        teardown_latex_dir()

def test_full_xelatex_writing():
    """
    Full run of the `xelatex` (XeLaTeX) pseudo-writer.
    """
    try:
        setup_latex_dir('fr-xelatex-full-')
        io = support.CapturingIo()
        io.source = support.get_utf8_fixture()
        rc = main.commandline(['xelatex',
                               '--lang=sv',
                               '--template=%s' % latex_tmp('template.tex')],
                              io=io)
        if rc == errno.ENOSYS:
            pytest.skip('xelatex not present on system')

        check_pdf_result(rc, io)
    finally:
        teardown_latex_dir()

def test_full_rtf_writing():
    """
    Full run of the `rtf` (Microsoft Rich Text) writer.
    """
    io = support.CapturingIo()
    io.source = support.get_utf8_fixture()
    rc = main.commandline(['rtf', '--lang=sv'], io)
    # XXX Only sanity check yet.
    assert_equals(rc, 0)

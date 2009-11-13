.. -*- mode: rst -*-
.. -*- Coding: utf-8 -*-

`Flexirest` is a project that was born out of the authors long-running
interest for reStructuredText_, and the idea of writing everyday
documents like letters, invoices and other simple documents in this
way.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

`Flexirest` tries to strike a middle ground between docutils_ own
command line tool chain (`rst2html` et al), that I find a little to
minimalistic and Sphinx_, that I find very nice but a little heavy to
use for a quickie document like a random letter or some such.

.. _docutils: http://docutils.sourceforge.net/
.. _Sphinx: http://sphinx.pocoo.org/

In short, the goal of `flexirest` is to enable you to use the `reST`
format for everyday documents instead of a word processor or similar
with minimal fuzz. Hence you get to stay in the comfy environment of
your text editor and tool chain. And you can check in your docs *in text
format* into your version control system of choice. And, if used
correctly, you get to reuse a couple of stylings that you only need to
create once.

There are some modestly advanced tricks you can do too, primarily
writing your own `docutils` roles_, but I wouldn't consider those the
major points of flexirest.

.. _roles: http://docutils.sourceforge.net/docs/howto/rst-roles.html

For more information on how to operate `flexirest`, see the
`quick manual`_.

.. _quick manual: quick-manual.html
.. _setuptools: http://pypi.python.org/pypi/setuptools

Changes
-------

0.8.2
+++++

* A mechanism of two-stage writing used to support a new writer,
  `latex2pdf` that renders directly to PDF via LaTeX if a suitable
  executable is available on the host system.
* `--infile` option to specify input from a file
* `--outfile` option to specify output to a file
* `--dump-parts` option to inspect output from different `docutils`
  parts.
* `--list-writer` option to list available writers on the host system.
* No traceback when specifying a non-existant writer
* All writers have at least the minimal template (`%(whole)s`)
* Switch to `Distribute` instead of `setuptools` for development and
  packaging.
* Many small bugfixes and stability improvements

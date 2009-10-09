import itertools
import os
import sys

from docutils import writers
from docutils.parsers.rst import roles
from docutils.core import publish_parts

__docformat__ = 'reStructuredText'

# XXX
"""
An iterator of all legal writer names.

Beware: the _writer_aliases dict is undocumented and marked as
private! We should find out a better way to produce this list.
"""
# XXX Add planned 'pseudo-writers' here
all_writers = lambda: itertools.chain(writers._writer_aliases.keys(),
                              writers._writer_aliases.values())

def _register_roles(conf):

    """
    Registers roles to be used in this run.

    `conf` - configuration module.
    """

    for rolecand, rolename in ((getattr(conf, role), role) for role in
                   dir(conf) if role.startswith('role_')):
        if callable(rolecand):
            roles.register_canonical_role(rolename[5:], rolecand)

def _dump_parts(writer_name, parts, out):

    """
    Writes a mini-report on what parts where created by the specified
    `docutils` writer (intended for human consumption).

    `parts` - parts `dict` created by `docutils.core.publish_parts()`
    `out` - output stream to write to.
    """

    title = "Parts created by the docutils writer '%s'" % writer_name
    out.write(title + os.linesep)
    out.write(len(title) * '-')
    out.write(2 * os.linesep)
    out.write('Part keys: ' + 2 * os.linesep)
    out.write(os.linesep.join(parts.keys()))
    out.write(2 * os.linesep)
    for part in parts:
        out.write("Value of part '%s':%s" % (part, os.linesep))
        out.write(parts[part] + os.linesep)
        out.write(80*'-'+os.linesep)
        out.write(os.linesep)

def render(source, destination, conf, options, template, writer_name):

    """API entry point.

    A call expected to succed must provide all parameters. See
    flexirest.main.commandline() to find sensible defaults.

    `source` - file-like object to read input from.
    `destination` - file-like object (needs at least `.write()` and `.flush()`
                  methods.
    `conf` - configuration module.
    `options` - commandline options
    `template` - the template to enter the results of `publish_parts()` into.
               (needs to support formatting with the '..' % {} technique.)
    `writer_name` - name of the `docutils` writer to use.
    """

    _register_roles(conf)

    # The .read().decode(..) chain below is a little inefficient, but
    # this is supposed to be a quite modest tool, so I'll just leave
    # it be for now..
    parts = publish_parts(
        source=source.read().decode('utf8'),
        writer_name=writer_name,
        settings_overrides=dict(), # Invent something nice for this..
    )

    parts['lang'] = options.lang

    if writer_name == 'html':
        parts['html_head'] = parts['html_head'] % ('utf-8',)
        parts['html_prolog'] = parts['html_prolog'] % ('utf-8',)

    if options.dump_parts:
        _dump_parts(writer_name, parts, destination)
    else:
        destination.write( (template % parts).encode("utf-8") )
        destination.flush()

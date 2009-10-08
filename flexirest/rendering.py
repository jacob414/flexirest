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

def render(source, destination, conf, lang, template, writer_name):

    """API entry point.

    A call expected to succed must provide all parameters. See
    flexirest.main.commandline() to find sensible defaults.

    `source` - file-like object to read input from.
    `destination` - file-like object (needs at least `.write()` and `.flush()`
                  methods.
    `conf` - configuration module.
    `lang` - language code of output.
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

    if writer_name == 'html':
        parts['html_head'] = parts['html_head'] % ('utf-8',)
        parts['html_prolog'] = parts['html_prolog'] % ('utf-8',)
        parts['lang'] = lang

    destination.write( (template % parts).encode("utf-8") )
    destination.flush()

import os
import sys

from docutils.parsers.rst import roles
from docutils.core import publish_parts

def render(source, destination, conf, lang, template, writer_name):

    """API entry point.

    A call expected to succed must provide all parameters. See
    flexirest.main.commandline() to find sensible defaults.

    source - file-like object to read input from.
    destination - file-like object (needs at least `.write()` and `.flush()`
                  methods.
    conf - configuration module.
    lang - language code of output.
    template - the template to enter the results of `publish_parts()` into.
               (needs to support formatting with the '..' % {} technique.)
    writer_name - name of the `docutils` writer to use.
    """

    for rolecand, rolename in ((getattr(conf, role), role) for role in
                   dir(conf) if role.startswith('role_')):
        if callable(rolecand):
            roles.register_canonical_role(rolename[5:], rolecand)

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

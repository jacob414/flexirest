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
all_writers = lambda: sorted(set(itertools.chain(writers._writer_aliases.keys(),
                              writers._writer_aliases.values())))

def _register_roles(conf):

    """
    Registers roles to be used in this run.

    `conf` - configuration module.
    """

    for rolecand, rolename in ((getattr(conf, role), role) for role in
                   dir(conf) if role.startswith('role_')):
        if callable(rolecand):
            roles.register_canonical_role(rolename[5:], rolecand)

class Render(object):

    def __init__(self, conf, options, template, writer_name):
        self.conf = conf
        self.options = options
        self.template = template
        self.writer = writer_name

    def _build_settings(self):
        _register_roles(self.conf)
        builderfn = getattr(self, '_build_%s_settings' % self.writer, False)
        if builderfn:
            return builderfn()
        return {}

    def dump_parts(self, source, destination):
        """
        Writes a mini-report on what parts where created by the specified
        `docutils` writer (intended for human consumption).

        `parts` - parts `dict` created by `docutils.core.publish_parts()`
        `out` - output stream to write to.
        """

        title = "Parts created by the docutils writer '%s'" % self.writer
        destination.write(title + os.linesep)
        destination.write(len(title) * '-')
        destination.write(2 * os.linesep)
        destination.write('Part keys: ' + 2 * os.linesep)

        parts = self.publish_parts(source)
        destination.write(os.linesep.join(parts.keys()))
        destination.write(2 * os.linesep)
        for part in parts:
            destination.write("Value of part '%s':%s" % (part, os.linesep))
            destination.write(parts[part] + os.linesep)
            destination.write(80*'-'+os.linesep)
            destination.write(os.linesep)

    def publish_parts(self, source):
        # The .read().decode(..) chain below is a little inefficient, but
        # this is supposed to be a quite modest tool, so I'll just leave
        # it be for now..
        parts = publish_parts(
            source=source.read().decode('utf8'),
            writer_name=self.writer,
            settings_overrides=self._build_settings(),
        )
        parts['lang'] = self.options.lang
        return parts

    def render(self, source, destination):
        parts = self.publish_parts(source)
        destination.write( (self.template % parts).encode("utf-8") )
        destination.flush()

    def _build_html_settings(self):
        return {}

def render(source, destination, conf, options, template, writer_name):

    """API entry point (helper for the most obvious case).

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

    renderer = Render(conf, options, template, writer_name)
    renderer.render(source, destination)

def dump_parts(source, destination, conf, options, template, writer_name):

    """API entry point for the `dump_parts` option.

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

    renderer = Render(conf, options, template, writer_name)
    renderer.dump_parts(source, destination)

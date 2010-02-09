import itertools
import os
import sys

from docutils import writers
from docutils.parsers.rst import roles
from docutils.core import publish_parts

__docformat__ = 'reStructuredText'

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
    """
    The `Render` object is a (somewhat) stateful representation of the
    rendering process. It's main purpose is to run the rendering
    stepwise, therefore enabling the two-step writing mechanism.
    """

    def __init__(self, strategy, conf, options, template):
        self.conf = conf
        self.options = options
        self.template = template
        strategy.options = options
        self.strategy = strategy

    def dump_parts(self, io):
        """
        Writes a mini-report on what parts where created by the specified
        `docutils` writer (intended for human consumption).

        `parts` - parts `dict` created by `docutils.core.publish_parts()`
        `out` - output stream to write to.
        """

        # XXX refactor with Tempita
        title = "Parts created by the docutils writer '%s'" % self.strategy.name
        io.say(title + os.linesep)
        io.say(len(title) * '-')
        io.say(2 * os.linesep)
        io.say('Part keys: ' + 2 * os.linesep)

        parts = self.publish_parts(io)
        io.say(os.linesep.join(sorted(parts.keys())))
        io.say(2 * os.linesep)
        for part in parts:
            io.say("Value of part '%s':%s" % (part, os.linesep))
            io.say(parts[part].encode('utf-8') + os.linesep)
            io.say(80*'-'+os.linesep)
            io.say(os.linesep)

    def publish_parts(self, io):
        # The .read().decode(..) chain below is a little inefficient..
        _register_roles(self.conf)
        parts = publish_parts(
            source = io.source.read().decode('utf-8'), # XXX utf-8 hardcoded
            writer=self.strategy.writer_object(),
            settings_overrides=self.strategy.settings,
        )
        parts['lang'] = self.options.lang
        return parts

    def render(self, io):
        parts = self.publish_parts(io)
        self.strategy.postprocess(parts, self.template, io.destination)
        io.destination.flush()

def render(strategy, io, conf, options, template):
    """
    API entry point (helper for the most obvious case).

    A call expected to succed must provide all parameters. See
    flexirest.main.commandline() to find sensible defaults.

    `stragegy` - writing strategy
    `io` - input/output handler
    `conf` - configuration module.
    `options` - commandline options
    `template` - the template to enter the results of `publish_parts()` into.
               (needs to support formatting with the '..' % {} technique.)
    """

    renderer = Render(strategy, conf, options, template)
    renderer.render(io)

def dump_parts(strategy, io, conf, options, template):
    """
    API entry point for the `dump_parts` option.

    A call expected to succed must provide all parameters. See
    flexirest.main.commandline() to find sensible defaults.

    `strategy`- writing strategy
    `io` - input/output handler
    `conf` - configuration module.
    `options` - commandline options
    `template` - the template to enter the results of `publish_parts()` into.
               (needs to support formatting with the '..' % {} technique.)
    """

    renderer = Render(strategy, conf, options, template)
    renderer.dump_parts(io)

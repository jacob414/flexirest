from __future__ import with_statement

import os
import sys
import optparse
import imp

from flexirest import meta
from flexirest.util import StdoutConsole

from docutils.parsers.rst import roles
from docutils.core import publish_parts

GLOBAL_USAGE = 'flexirest <options>'

DEFAULT_TEMPLATE = u"""%(html_prolog)s
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
%(html_head)s
</head>
<body>
%(html_body)s
</body>
</html>
"""

def _import(modname):
    return __import__(modname)

def commandline(args=None, console=None, source=None, destination=None):
    if console is None:
        console = StdoutConsole()
    if args is None:
        args = sys.argv[1:]
    if source is None:
        source = sys.stdin
    if destination is None:
        destination = sys.stdout
    parser = optparse.OptionParser(usage = GLOBAL_USAGE,
                                   description = meta.CMDLINE_DESC)

    parser.add_option('-v',
                      '--version',
                      action='store_true',
                      dest='version',
                      default=False,
                      help='print version and exit')
    parser.add_option('-t',
                      '--template',
                      action='store',
                      dest='template',
                      default=False,
                      help='apply source into this template')
    parser.add_option('-r',
                      '--roles',
                      dest='roles',
                      default=False,
                      help='apply source into this template')
    parser.add_option('-w',
                      '--writer',
                      dest='writer',
                      default=False,
                      help='use docutils writer named "writer"')

    options, args = parser.parse_args(args)
    if options.version:
        console.write("flexirest version '%s'" % meta.VERSION)
        return 0
    if options.template:
        with file(options.template, 'r') as fp:
            template = fp.read()

    writer = options.writer or 'html'
    if options.writer:
        writer=options.writer
    else:
        template = DEFAULT_TEMPLATE

    options, args = parser.parse_args(args)
    if options.version:
        console.write("flexirest version '%s'" % meta.VERSION)
        return 0
    if options.template:
        with file(options.template, 'r') as fp:
            template = fp.read()
    else:
        template = DEFAULT_TEMPLATE

    if options.roles:
        roles_mod = _import(options.roles)
    else:
        roles_mod = _import('roles')

    for rolecand, rolename in ((getattr(roles_mod, role), role) for role in
                   dir(roles_mod) if role.startswith('role_')):
        if callable(rolecand):
            roles.register_canonical_role(rolename, rolecand)

    # The .read().decode(..) chain below is a little inefficient, but
    # this is supposed to be a quite modest tool, so I'll just leave
    # it be for now..
    parts = publish_parts(
        source=source.read().decode('utf8'),
        writer_name=options.writer or 'html',
        settings_overrides=dict(), # Invent something nice for this..
    )

    return 0

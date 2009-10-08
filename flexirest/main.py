from __future__ import with_statement

import os
import sys
import optparse
import imp

from flexirest import rendering, defaults, meta
from flexirest.util import StdoutConsole

cmdline_options = (
    ('-v', '--version', dict(action='store_true',
                             dest= 'version',
                             default=False,
                             help='print version and exit')),
    ('-t', '--template', dict(action='store',
                              dest='template',
                              default=False,
                              help='apply source into this template')),
    ('-l', '--lang', dict(action='store',
                          dest='lang',
                          default='en',
                          help='specify language (both input and output)')),
    ('-c', '--config', dict(dest='config',
                            default=False,
                            help='apply source into this template')),
    ('-w', '--writer', dict(dest='writer',
                            default=False,
                            help='use docutils writer named "writer"')),
)

def _import(modname, onFailRaise=True):
    try:
        return __import__(modname)
    except ImportError:
        if onFailRaise:
            raise
        return imp.new_module(modname)

def parse_commandline(args):
    parser = optparse.OptionParser(usage = meta.CMDLINE_USAGE,
                                   description = meta.CMDLINE_DESC)

    for opt in cmdline_options:
        parser.add_option(opt[0], opt[1], **opt[2])

    return parser.parse_args(args)


def commandline(args=None, console=None, source=None, destination=None):
    if console is None:
        console = StdoutConsole()
    if args is None:
        args = sys.argv[1:]
    if source is None:
        source = sys.stdin
    if destination is None:
        destination = sys.stdout

    options, args = parse_commandline(args)

    if options.version:
        console.write("flexirest version '%s'" % meta.VERSION)
        return 0

    writer_name = options.writer or 'html'

    if options.template:
        with open(options.template, 'r') as fp:
            template = fp.read()
    else:
        template = defaults.templates[writer_name]

    sys.path.append(os.getcwd())
    if options.config:
        confmod = _import(options.config)
    else:
        confmod = _import('flexiconf', False)

    return rendering.render(source,
                            destination,
                            confmod,
                            options.lang,
                            template,
                            writer_name)

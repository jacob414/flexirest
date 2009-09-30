from __future__ import with_statement

import os
import sys
import optparse
import imp

from flexirest import rendering, defaults, meta
from flexirest.util import StdoutConsole

def _import(modname, onFailRaise=True):
    try:
        return __import__(modname)
    except ImportError:
        if onFailRaise:
            raise
        return imp.new_module(modname)

def commandline(args=None, console=None, source=None, destination=None):
    if console is None:
        console = StdoutConsole()
    if args is None:
        args = sys.argv[1:]
    if source is None:
        source = sys.stdin
    if destination is None:
        destination = sys.stdout
    parser = optparse.OptionParser(usage = meta.CMDLINE_USAGE,
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
    parser.add_option('-l',
                      '--lang',
                      action='store',
                      dest='lang',
                      default='en',
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

    writer_name = options.writer or 'html'

    if options.template:
        with open(options.template, 'r') as fp:
            template = fp.read()
    else:
        template = defaults.templates[writer_name]

    sys.path.append(os.getcwd())
    if options.roles:
        confmod = _import(options.roles)
    else:
        confmod = _import('flexiconf', False)

    return rendering.render(source,
                            destination,
                            confmod,
                            options.lang,
                            template,
                            writer_name)

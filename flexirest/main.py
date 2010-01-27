from __future__ import with_statement

import os
import sys
import optparse
import imp
import errno

from functools import partial

from aspektratio.cli import dispatch, DefaultAction, ShowVersion, SilentExit
from aspektratio.io import BufferedFile

from flexirest import world, rendering, defaults, meta, strategies
from flexirest.util import StdoutConsole

_cmdline_options = (
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
    ('-r', '--list-writers', dict(action='store_true',
                                  dest='list_writers',
                                  default=False,
                                  help='print a list of all writers and quit')),
    ('-d', '--dump-parts', dict(action='store_true',
                                dest='dump_parts',
                                default=False,
                                help='Dump docutils parts produced by specified writer')),
    ('-i', '--infile', dict(action='store',
                            dest='infile',
                            default=False,
                            help='read input from this file')),
    ('-o', '--outfile', dict(action='store',
                             dest='outfile',
                             default=False,
                             help='write output to this file')),
    ('-s', '--styles', dict(action='store',
                            dest='resources',
                            default=False,
                            help='resource files for this writing task (LaTeX only)')),
)

_print_and_quit_options = set(('version', 'list_writers'))

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

    for opt in _cmdline_options:
        parser.add_option(opt[0], opt[1], **opt[2])

    return parser.parse_args(args)

def commandline(args=None, console=None, source=None, destination=None):
    if console is None:
        console = StdoutConsole()
    if args is None:
        args = sys.argv[1:]

    options, args = parse_commandline(args)

    # XXX or maybe we shouldn't quit, just continue after we answered
    # out simple question?
    opts_w_vals = set( (opt for opt, val in options.__dict__.iteritems() if val) )
    if opts_w_vals & _print_and_quit_options:
        if options.version:
            console.write("flexirest version %s" % meta.VERSION)
        if options.list_writers:
            for available_writer in world.all_writers:
                console.write(available_writer)

        return 0

    # source parameter of `commandline()` always wins
    if source is None:
        if options.infile:
            # XXX File not found will just dump traceback to stderr
            source = open(os.path.expanduser(options.infile), 'r')
        else:
            source = sys.stdin

    # destination parameter of `commandline()` always wins
    if destination is None:
        if options.outfile:
            # XXX Create error will just dump traceback to stderr
            destination = BufferedFile(options.outfile)
        else:
            destination = sys.stdout

    writer_name = options.writer or 'html'
    if writer_name not in world.all_writers:
        sys.stderr.write("flexirest: '%s' is not a valid writer%s" %
                              (writer_name, os.linesep))
        return errno.EINVAL

    if options.template:
        with open(os.path.expanduser(options.template), 'r') as fp:
            template = fp.read()
    else:
        template = defaults.templates[writer_name]

    sys.path.append(os.getcwd())
    if options.config:
        confmod = _import(options.config)
    else:
        confmod = _import('flexiconf', False)

    if options.dump_parts:
        rendering.dump_parts(source,
                             destination,
                             confmod,
                             options,
                             template,
                             writer_name,)
    else:
        rendering.render(source,
                         destination,
                         confmod,
                         options,
                         template,
                         writer_name,)

    # XXX Way to simple way to treat return codes
    return 0

class Io(object):
    """
    A composite that represents input/output channels that the program
    need:

    * The user's console (typically `sys.stdout`)
    * The error channel (typically `sys.stderr`)
    * The source (input file/`sys.stdin`)
    * The destination (output file/`sys.stdout`)
    """

    def __init__(self, stdin=sys.stdin, stderr=sys.stderr):
        self.stderr = stderr
        self.console = sys.stdout
        self.source = sys.stdin
        self.destination = sys.stdout

    def line(self, msg):
        """
        Convinience method that formats a line of output.
        """
        return '%s%s' % (msg, os.linesep)

    def say(self, msg):
        """
        Tell the user something (typically on `sys.stdout`)
        """
        self.console.write(self.line(msg))

    def complain(self, msg):
        """
        Inform the user about error conditions (typically on `sys.stderr`)
        """
        self.stderr.write(self.line(msg))

    def out(self, data):
        """
        Output data to destination (output file/`sys.stdout`).
        """
        self.destination.write(data)

def show_status(io, args):
    """
    Shows a summary of which writers are present and functional on the
    user's system. (TODO: with small instructions on how to fix
    non-functional writers)
    """
    functional, nonfunctional = strategies.check_writers()

    linefn = lambda n, desc: (lambda: '  %s\t%s' % (n, desc))().expandtabs(16)

    def lines(strategies):
        for name in sorted(strategies):
            yield linefn(name, strategies[name].description)

    import tempita
    tmpl = tempita.Template(meta.STATUS,
                            namespace={'functional': lines(functional),
                                       'nonfunctional': lines(nonfunctional)})
    io.say(tmpl.substitute())
    return 0

def show_info(io):
    """
    Writes brief information about the program when it's run with no
    parameters.
    """
    io.say(meta.INFO % meta.VERSION)
    show_status(io, ())
    return 0

def show_version(io):
    io.say(meta.VERSION)
    return 0

def writer_action(io, name, Strategy, options, args):
    """
    Called by `commandline()` as a result of sub-command
    dispatching. At this point the name of the writer is in `name` and
    the strategy that should be send to the `rendering` module is in
    the parameter `Strategy`.

    The return value of this function will be the command line's
    return value.
    """
    inopen = lambda n: open(os.path.expanduser(n), 'r')
    if len(args) == 1:
        # Only infile
        io.source = inopen(args[0])
        io.destination = sys.stdout
    elif len(args) > 1:
        io.source = inopen(args[0])
        io.destination = BufferedFile(os.path.expanduser(args[1]))

    sys.path.append(os.getcwd())
    if options.config:
        confmod = _import(options.config)
    else:
        confmod = _import('flexiconf', False)

    if options.template:
        with open(os.path.expanduser(options.template), 'r') as fp:
            template = fp.read()
    else:
        template = defaults.templates[writer_name]

    if options.dump_parts:
        rendering.dump_parts(io.source,
                             io.destination,
                             confmod,
                             options,
                             template,
                             name)
    else:
        rendering.render(io.source,
                         io.destination,
                         confmod,
                         options,
                         template,
                         name)

    # XXX Way to simple way to treat return codes
    return 0

def options(console, name, Strategy, args):
    """
    Calls the strategy to add writer-specific command line options.
    """
    parser = optparse.OptionParser(usage='usage',
                                   description='description')
    Strategy.add_options(parser)
    return parser

def commandline_new(args=None, io=None):
    """
    Entry point for the command line script.
    """
    if io is None:
        io = Io()
    if args is None:
        args = sys.argv[1:]

    actions = {
        'st': partial(show_status, io),
        'status': partial(show_status, io)
    }

    for name, Strategy in strategies.possible_writers.iteritems():
        actions[name] = (partial(writer_action, io, name, Strategy),
                         partial(options, io, name, Strategy))

    try:
        return dispatch(actions, args)
    except DefaultAction:
        show_info(io)
        return 0
    except ShowVersion:
        show_version(io)
        return 0
    except SilentExit:
        return 0

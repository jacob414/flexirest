from __future__ import with_statement

import os
import sys
import optparse
import imp
import errno
import platform

from functools import partial

import flexirest

from flexirest.cli import (dispatch, DefaultAction, ShowVersion, SilentExit,
                           UnknownSubcommand)
from flexirest.io import BufferedFile

from flexirest import rendering, defaults, strategies
from flexirest.util import shellopen, StdoutConsole

def _import(modname, onFailRaise=True):
    try:
        return __import__(modname)
    except ImportError:
        if onFailRaise:
            raise
        return imp.new_module(modname)

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
    tmpl = tempita.Template(flexirest.STATUS,
                            namespace={'functional': lines(functional),
                                       'nonfunctional': lines(nonfunctional)})
    io.say(tmpl.substitute())
    return 0

def show_info(io):
    """
    Writes brief information about the program when it's run with no
    parameters.
    """
    io.say(flexirest.INFO % flexirest.VERSION)
    show_status(io, ())
    return 0

def show_version(io):
    io.say(flexirest.VERSION)
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
    dest = None
    if options.outfile:
        dest = shellopen(options.outfile, 'w')
        if len(args) == 1:
            io.source = shellopen(args[0], 'r')
    else:
        if len(args) == 1:
            # Only infile
            io.source = shellopen(args[0], 'r')
        elif len(args) > 1:
            io.source = shellopen(args[0], 'r')
            dest = BufferedFile(os.path.expanduser(args[1]))

    if dest:
        io.destination = dest

    sys.path.append(os.getcwd())
    if options.config:
        confmod = _import(options.config)
    else:
        confmod = _import('flexiconf', False)

    tpath = getattr(options, 'template', False)
    if tpath:
        template = shellopen(tpath, 'r').read()
    else:
        template = defaults.templates[name]

    strategy = strategies.from_name(name)

    if options.dump_parts:
        rendering.dump_parts(strategy,
                             io,
                             confmod,
                             options,
                             template)
    else:
        rendering.render(strategy,
                         io,
                         confmod,
                         options,
                         template)

    # XXX Way to simple way to treat return codes
    return 0

def options(console, name, Strategy, args):
    """
    Calls the strategy to add writer-specific command line options.
    """
    parser = optparse.OptionParser(usage='usage',
                                   description='description')
    Strategy.add_options(parser)
    parser.add_option('-l', '--lang', action='store', dest='lang', default='en',
                      help='specify language (both input and output)')
    parser.add_option('-o', '--outfile', action='store', dest='outfile',
                      help='write output to this file')
    return parser

def commandline(args=None, io=None):
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
    except UnknownSubcommand, e:
        io.complain("flexirest: '%s' is not a valid writer" % e.subcmd)
        return errno.EINVAL
    except strategies.NonFunctionalStrategy, e:
        io.complain("flexirest: the '%s' writer is not functional on "
                    "your system" % e.name)
        io.complain("    (hint: %s)" % e.hint)
        return errno.ENOSYS
    except ShowVersion:
        show_version(io)
        return 0
    except SilentExit:
        return 0

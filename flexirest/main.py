import os
import sys
import optparse

from flexirest import meta
from flexirest.util import StdoutConsole

GLOBAL_USAGE = 'flexirest <options>'

def commandline(args=None, console=None):
    """
    The flexirest commandline entry point.
    """
    if console is None:
        console = StdoutConsole()
    if args is None:
        args = sys.argv[1:]
    parser = optparse.OptionParser(usage = GLOBAL_USAGE,
                                   description = meta.CMDLINE_DESC)

    parser.add_option('-v',
                      '--version',
                      action='store_true',
                      dest='version',
                      default=False,
                      help='print version and exit')
    options, args = parser.parse_args(args)
    if options.version:
        console.write("flexirest version '%s'" % meta.VERSION)
        return 0

    return 0

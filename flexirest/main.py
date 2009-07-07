import os
import sys

GLOBAL_USAGE = 'flexirest <options> <rst file>'

class StdioConsole(object):

    def __init__(self):
        self.out = sys.stdout

    def write(self, msg):
        self.out.write(msg + os.linesep)

def commandline(args=None, console=None):
    """
    The flexirest commandline entry point.
    """
    if console is None:
        console = StdioConsole()
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
        console.write("playlist version '%s'" % meta.VERSION)
        return 0

    return 0

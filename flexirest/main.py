import os
import sys
import optparse

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
    parser.add_option('-t',
                      '--template',
                      dest='template',
                      default=None,
                      help='apply source into this template')
    parser.add_option('-r',
                      '--roles',
                      dest='template',
                      default=None,
                      help='apply source into this template')

    options, args = parser.parse_args(args)
    if options.version:
        console.write("flexirest version '%s'" % meta.VERSION)
        return 0
    if options.template is None:
        template = DEFAULT_TEMPLATE
    if options.roles is not None:
        try:
            roles_mod = __import__(option.roles)
        except ImportError:
                pass

        role_names = (role[5:] for role in
                      dir(__import__(options.roles)) if role.startswith('role_'))


    return 0

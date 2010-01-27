from __future__ import with_statement

import os, sys, shutil, tempfile, subprocess, re
from cStringIO import StringIO

__docformat__ = 'reStructuredText'

class StdoutConsole(object):
    """
    Vaguely file-like object that immediately writes it output to
    `sys.stdout` followed by an os-appropriate `EOL`.
    """

    def __init__(self):
        self.out = sys.stdout

    def write(self, msg):
        self.out.write(msg + os.linesep)

class Duck(object):
    """Quack!"""

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __repr__(self):
        """
        Thanks to Chris Jones!
        """
        a = ', '.join('%s=%r' % i for i in self.__dict__.items())
        return '<%s object at 0x%x%s%s>' % (
                type(self).__name__, id(self), ': ' if a else '', a)

dash_rx = re.compile('-')
def legalize_it(name):
    return re.sub(dash_rx, name)

def add_bool(parser, shorter, longer, help):
    parser.add_option(shorter, longer,
                      action='store_true', dest=legalize_it(longer[2:]),
                      default=False, help=help)

from functools import partial

def default_option_adders(parser):
    return (partial(parser.add_option,
                    action='store_true',
                    default=False),
            partial(parser.add_option,
                    default=False) )

def has_program(*cmdline):
    """
    Tries to execute a program with optional options (passed as a list with
    the programs name first.
    """
    try:
        return subprocess.call(cmdline,
                               stdin=open(os.devnull, 'r'),
                               stdout=open(os.devnull, 'w'),
                               stderr=open(os.devnull, 'w'),
                               env=os.environ) == 0
    except OSError:
        return False


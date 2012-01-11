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

def shellopen(path, mode):
    """
    Opens a file according to shell conventions: '-' means `stdin`
    when opening `path` for reading, `stdout` when opening `path` for
    writing, otherwise open the path as a file with '~' meaing the
    users home directory (which would probably work so-so on Windows?).
    """
    if path == '-' and mode.startswith('r'):
        return sys.stdin
    elif path == '-' and mode.startswith('w'):
        return sys.stdout
    else:
        return open(os.path.expanduser(path), mode)

class substitute(object):
    """
    A context manager that takes the name of a globally reachable
    object (in the form of 'module.object', e.g. `sys.stdout`) and
    substitutes it with another object while the context manager is in
    effect.

    Example::

        >>> from StringIO import StringIO
        >>> capture = StringIO()
        >>> with substitute('sys.stdout', capture):
        ...     print('foo')
        >>> capture.getvalue()
        'foo\\n'

    or::

        >>> import os
        >>> with substitute('os.path.exists', lambda p: 'Yes indeedy!'):
        ...     assert os.path.exists('/no/such/path') == 'Yes indeedy!'
        >>> assert os.path.exists('/no/such/path') == False

    Exceptions are propagated after the value is restored::

        >>> import os
        >>> with substitute('os.environ', {}):
        ...    os.environ['PATH']
        Traceback (most recent call last):
        KeyError
    """

    def __init__(self, name, substitution):
        self.name = name
        self.substitution = substitution

    def __enter__(self):
        self.oldvalue, self._set = find_in_module(self.name)
        self._set(self.substitution)
        return self

    def __exit__(self, exc, value, tb):
        self._set(self.oldvalue)
        if tb is not None:
            raise(exc, value, tb)

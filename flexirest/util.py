from __future__ import with_statement

import os
import sys
import shutil
import tempfile
from cStringIO import StringIO

__docformat__ = 'reStructuredText'

class StdoutConsole(object):
    """Vaguely file-like object that immediately writes it output to
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

class BufferedFile(file):
    """File-like object that writes to an internal buffer. It will only
    write to the file system when it's `.close()` method is called
    **and** it has actually written something to itself.

    Inspired by `tempfile.SpooledTemporaryFile`, but with far less
    features (yagni.. for now it only supports writing, for example).
    """

    def __init__(self, path):
        self._buf = StringIO()
        self.path = path
        # Make shure that we seem open and functional..
        super(BufferedFile, self).__init__(os.devnull, 'wb')

    def write(self, data):
        self._buf.write(data)

    def flush(self):
        curdata = self._buf.getvalue()
        if len(curdata) > 0:
            with open(self.path, 'wb') as fp:
                fp.write(curdata)

    def close(self):
        self.flush()
        super(BufferedFile, self).close()

class TempDirectory(object):
    """A context-manager capable object that keeps an
    """

    def __init__(self, prefix=None):
        if prefix is None:
            prefix = 'tmp'
        self.prefix = prefix

    def manifest(self):
        """Actually create the temporary directory.
        """
        if hasattr(self, 'tmpdir'):
            raise RuntimeError('temporary directory already manifested')
        self.tmpdir = tempfile.mkdtemp(prefix=self.prefix)

    def cleanup(self):
        """Removes the temporary directory.
        """
        shutil.rmtree(self.tmpdir)

    def path(self, name):
        """Returns a file path inside this temporary directory.
        """
        return os.path.join(self.tmpdir, name)

    def put(self, name, content):
        """Put arbitrary content into a temporary file inside the
        temporary directory.
        """
        with self.open(name, 'w') as fp:
            fp.write(content)

    def open(self, name, mode):
        """Open a file in the temporary directory.
        """
        return open(self.path(name), mode)

    def copy(self, path):
        """Copy an existing file into the temporary directory.
        """
        shutil.copy(path, self.path(os.path.basename(path)))

    def __enter__(self):
        """Make this class context-manager capable."""
        self.manifest()
        return self

    def __exit__(self, type_, value, tb):
        """Make this class context-manager capable."""
        self.cleanup()

# -*- coding: utf-8 -*-

from __future__ import with_statement

import os, sys, shutil, tempfile

from cStringIO import StringIO

__docformat__ = 'reStructuredText'

class BufferedFile(file):
    """
    File-like object that writes to an internal buffer. It will only
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
    """
    A context-manager capable object that keeps an
    """

    def __init__(self, prefix=None):
        if prefix is None:
            prefix = 'tmp'
        self.prefix = prefix

    def manifest(self):
        """
        Actually create the temporary directory.
        """
        if hasattr(self, 'tmpdir'):
            raise RuntimeError('temporary directory already manifested')
        self.path = tempfile.mkdtemp(prefix=self.prefix)

    def cleanup(self):
        """
        Removes the temporary directory.
        """
        shutil.rmtree(self.path)

    def newpath(self, name):
        """
        Returns a file path inside this temporary directory.
        XXX: refactor name as *path, iterable with sub paths.
        """
        return os.path.join(self.path, name)

    def put(self, name, content):
        """
        Put arbitrary content into a temporary file inside the
        temporary directory.
        """
        with self.open(name, 'w') as fp:
            fp.write(content)

    def open(self, name, mode):
        """
        Open a file in the temporary directory.
        """
        return open(self.newpath(name), mode)

    def copy(self, path):
        """
        Copy an existing file into the temporary directory.
        """
        shutil.copy(path, self.newpath(os.path.basename(path)))

    def __enter__(self):
        """
        Make this class context-manager capable.
        """
        self.manifest()
        return self

    def __exit__(self, type_, value, tb):
        """
        Make this class context-manager capable.
        """
        self.cleanup()

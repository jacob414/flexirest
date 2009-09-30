import sys
from StringIO import StringIO

MINIMAL_FIXTURE = StringIO("""
=====
Title
=====
Text
""")

def getraise(callable, *args, **kwargs):
    """
    Calls `callable`, expecting an exception inheriting from
    StandardError (your exceptions *are* inheriting from
    StandardError, right?), with `*args` and `**kwargs` as parameters.

    Returns the results of `sys.exc_info()` as a result.

    Isn't there something built into nose that does this? I can't find
    it.

    >>> _type, exc, tb = getraise(open, '/no/such/path')
    >>> exc
    IOError(2, 'No such file or directory')
    >>>
    """
    try:
        callable(*args, **kwargs)
    except StandardError:
        return sys.exc_info()

class Capturer(object):
    """
    User by test_main to capture output from main.commandline(). The
    capturer is any object that supports a .write() method (`sys.stdout`
    would be used in production code).
    """
    def __init__(self):
        self.lines = []

    def write(self, msg):
        self.lines.append(msg)

    def flush(self):
        pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()

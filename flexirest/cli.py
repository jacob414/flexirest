import sys

class SilentExit(StandardError):
    """Exit the program silently (and with exit code 0)"""

class DefaultAction(SilentExit):
    """Show help"""

class ShowVersion(SilentExit):
    """Show version"""

class UnknownSubcommand(SilentExit):
    """Subcommand doesn't exist"""

    def __init__(self, subcmd):
        self.subcmd = subcmd

def dispatch(actions, args=None):
    """
    Helper to do a dispatch for a CLI-application in the style of
    `execname action` (e.g. the style of mercurial, subversion,
    apt-get etc). `actions` is a `dict` containing either a `callable`
    that should be called in response to the action, or a two
    callables, first the action itself and then another `callable`
    that returns a `optparse.OptionParser`, which will have it's
    `.parse_args()` method run and fed as arguments to the action.

    Simplest possible example::

       >>> dispatch({'a':lambda a: 'ok'}, ('a',))
       'ok'

    `dispatch()` have two special cases, the default action and the
    'version' case::

       >>> dispatch({}, ('help',))
       Traceback (most recent call last):
       DefaultAction

    The default action is also raised if the `args` parameter is empty::

       >>> dispatch({}, ())
       Traceback (most recent call last):
       DefaultAction

    and::

       >>> dispatch({}, ('version',))
       Traceback (most recent call last):
       ShowVersion

    The code that uses `dispatch()` should catch these exceptions and
    print your default help text and your program's version,
    respectively.
    """
    if args is None:
        args = sys.argv[1:]

    if len(args) == 0 or args[0] in ('-h', '--help', 'help'):
        raise DefaultAction
    elif args[0] in ('-v', '--version', 'version'):
        raise ShowVersion

    subcmd = args[0]
    try:
        action = actions[subcmd]
    except KeyError:
        raise UnknownSubcommand(subcmd)

    if hasattr(action, '__call__'):
        return action(args[1:])
    else:
        action, getparser = action
        args = args[1:]
        return action(*getparser(args).parse_args(args))

if __name__ == '__main__':
    import doctest
    doctest.testmod()


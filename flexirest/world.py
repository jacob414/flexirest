__docformat__ = 'reStructuredText'

from itertools import chain

class NormalWorld(object):
    """
    Gathers information about the state of the 'world' `flexirest`
    runs in this time.
    """

    def __init__(self):
        self._all_writers = None

    @property
    def all_writers(self):
        if self._all_writers is None:
            from flexirest import strategies
            self._all_writers = dict(((name, strategy) for name, strategy
                                     in strategies.functional_strategies()))
        return self._all_writers

__docformat__ = 'reStructuredText'

from itertools import chain

from flexirest import strategies
from docutils import writers

class NormalWorld(object):
    """
    Gathers information about the state of the 'world' `flexirest`
    runs in this time.
    """

    def __init__(self):
        self._gather_writers()

    def _gather_writers(self):
        self.all_writers = dict(((name, strategy) for name, strategy
                                 in strategies.functional_strategies()))

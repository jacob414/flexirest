from itertools import chain

from docutils import writers

from flexirest import tex

__docformat__ = 'reStructuredText'

class GeneralWriterStrategy(object):

    def __init__(self, name):
        self.name = name

    @property
    def settings(self):
        """
        This method should return a `dict` with additional settings
        for the writer (will be passed on to the appropriate
        `docutils` publisher.
        """
        return {}

    def postprocess(self, text, destination):
        """
        With this method, a post-processing step can be added to the
        writing strategy (for example, the latex2pdf writer invokes
        `pdflatex` here.
        """
        destination.write( text.encode("utf-8") )

    def isfunctional(self):
        """
        This method should try to determine if the strategy is a
        viable one (can the writer class be instantiated, does helper
        executables exists, other considerations?)
        """
        try:
            self.writer_object()
        except ImportError:
            return False
        return True

    def writer_object(self):
        """
        Return the `docutils` -compliant `Writer` object to send to
        the `docutils` publisher.
        """
        # Assume this writer is a built-in.
        return writers.get_writer_class(self.name)()

class LatexStrategy(GeneralWriterStrategy):

    @property
    def settings(self):
        return {'output_encoding': 'utf-8', # XXX should probably support more..
                'language_code': self.options.lang}

class Latex2PDFStrategy(LatexStrategy):

    def postprocess(self, latex, destination):
        """
        Invokes `pdflatex` with the help of the `flexirest.tex` module.
        """
        pdf = tex.latex2pdf(latex)
        destination.write(pdf)

    def isfunctional(self):
        # XXX Try to execute `pdflatex -version` (Issue #13)
        return True

    def writer_object(self):
        """
        Return a LaTeX `docutils` writer object.
        """
        return writers.get_writer_class('latex')()

# XXX Beware: the _writer_aliases dict is undocumented and marked as
# private! In theory we should find out a better way to produce this
# list, but right now I don't see any way of doing that.
builtin_writers = dict.fromkeys(set(chain(writers._writer_aliases.keys(),
                                          writers._writer_aliases.values())),
                                GeneralWriterStrategy)
builtin_writers['latex'] = LatexStrategy
builtin_writers['latex2e'] = LatexStrategy

pseudo_writers = {'latex2pdf': Latex2PDFStrategy}

external_writers = {} # XXX Future..

def functional_strategies():
    for name, Strategy in chain(builtin_writers.items(),
                                pseudo_writers.items(),
                                external_writers.items()):
        strategy = Strategy(name)
        if strategy.isfunctional():
            yield name, strategy
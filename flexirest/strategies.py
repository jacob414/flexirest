import os
from itertools import chain

from docutils import writers

from flexirest import util, tex

__docformat__ = 'reStructuredText'

class GeneralWriterStrategy(object):

    description = 'Not shure what this does'
    writer_name = None

    @property
    def settings(self):
        """
        This method should return a `dict` with additional settings
        for the writer (will be passed on to the appropriate
        `docutils` publisher.
        """
        return {}

    def postprocess(self, parts, template, destination):
        """
        With this method, a post-processing step can be added to the
        writing strategy (for example, the latex2pdf writer invokes
        `pdflatex` here.
        """
        destination.write( (template.decode('utf-8') % parts).encode('utf-8') )


    @classmethod
    def isfunctional(cls):
        """
        This method should try to determine if the strategy is a
        viable one (can the writer class be instantiated, does helper
        executables exists, other considerations?)
        """
        try:
            cls.writer_object()
        except ImportError:
            return False
        return True

    @classmethod
    def writer_object(cls):
        """
        Return the `docutils` -compliant `Writer` object to send to
        the `docutils` publisher.
        """
        # Assume this writer is a built-in.
        return writers.get_writer_class(cls.writer_name)()

class HtmlStrategy(GeneralWriterStrategy):

    description = 'HTML (docutils builtin)'
    writer_name = 'html4css'

class PseudoXmlStrategy(GeneralWriterStrategy):

    description = "'pseudo xml' (docutils builtin)"
    writer_name = 'pseudoxml'

class DocutilsXmlStrategy(GeneralWriterStrategy):

    description = 'docutils own XML (docutils built in)'
    writer_name = 'docutils_xml'

class S5HtmlStrategy(GeneralWriterStrategy):

    description = 'Renders S5 HTML (docutils built in)'
    writer_name = 's5_html'

class LatexStrategy(GeneralWriterStrategy):

    description = 'LaTeX (docutils built in)'
    writer_name = 'latex2e'

    @property
    def settings(self):
        settings = {'language': self.options.lang}
        if self.options.resources:
            settings['stylesheet'] = self.options.resources
        enc = getattr(self, 'encoding', False)
        if enc:
            settings['output_encoding'] = enc
        return settings

class LatexPostProcessingStrategy(LatexStrategy):

    def postprocess(self, parts, template, destination):
        """
        Invokes `pdflatex` with the help of the `flexirest.tex` module.
        """
        pdf = tex.run_program(self.program, template % parts)
        destination.write(pdf)

    @classmethod
    def isfunctional(cls):
        # XXX Try to execute the program with the '-version' switch (Issue #13)
        if super(LatexPostProcessingStrategy, cls).isfunctional():
            return util.has_program(cls.program, '-version')
        return True

class Latex2PDFStrategy(LatexPostProcessingStrategy):

    description = 'PDF via LaTeX and `pdflatex`'

    # XXX improvement idea: make this a property that optionally
    # XXX gets the program path from some configuration.
    program = 'pdflatex'

    encoding = 'utf-8' # XXX Hardcoded, think about better way

class XeLaTeXStrategy(LatexPostProcessingStrategy):

    description = 'PDF via LaTeX and `xelatex`'

    # XXX see XXX in Latex2PDFStrategy
    program = 'xelatex'

    # encoding is implicitly unicode in XeLaTeX

class OdtStrategy(GeneralWriterStrategy):

    description = 'OpenDocument'

    def postprocess(self, parts, template, destination):
        destination.write(parts['whole'])

    @classmethod
    def writer_object(cls):
        from odtwriter import Writer
        return Writer()

class RtfStrategy(GeneralWriterStrategy):

    description = "Microsoft's Rich Text Format ('RTF')"

    @classmethod
    def writer_object(cls):
        from flexirest.rtf import RtfWriter
        return RtfWriter()

# XXX Beware: the _writer_aliases dict is undocumented and marked as
# private! In theory we should find out a better way to produce this
# list, but right now I don't see any way of doing that.
builtin_writers = dict.fromkeys(set(chain(writers._writer_aliases.keys(),
                                          writers._writer_aliases.values())),
                                GeneralWriterStrategy)
builtin_writers['latex'] = LatexStrategy
builtin_writers['latex2e'] = LatexStrategy

pseudo_writers = {'latex2pdf': Latex2PDFStrategy,
                  'xelatex': XeLaTeXStrategy}

external_writers = {'odt': OdtStrategy,
                    'rtf': RtfStrategy}

def functional_strategies():
    for name, Strategy in chain(builtin_writers.items(),
                                pseudo_writers.items(),
                                external_writers.items()):
        strategy = Strategy()
        yield name, Strategy

possible_writers = {
    'latex': LatexStrategy,
    'docutils_xml': DocutilsXmlStrategy,
    'pdflatex': Latex2PDFStrategy,
    'xelatex': XeLaTeXStrategy,
    'odt': OdtStrategy,
    's5': S5HtmlStrategy,
    'html': HtmlStrategy,
    'pseudoxml': PseudoXmlStrategy,
    'rtf': RtfStrategy,
}

def check_writers():
    functional = nonfunctional = {}
    for name, Strategy in possible_writers.iteritems():
        print('NAME: %s' % name)
        if Strategy.isfunctional():
            functional[name] = Strategy
        else:
            nonfunctional[name] = Strategy

    return functional, nonfunctional

# def functional_strategies():
#     for name, Strategy in possible_writers.iteritems():
#         strategy = Strategy()
#         if strategy.isfunctional():
#             yield name, strategy

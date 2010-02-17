import os
from itertools import chain

from docutils import writers

from flexirest import util, tex

__docformat__ = 'reStructuredText'

template_option = ('template', (str, '-t', '--template',
                             'apply source into this template'))
stylesheets_option = ('stylesheets', (str, '-s', '--styles',
                                      'stylesheet(s) to use in this rendering'))

class NonFunctionalStrategy(StandardError):
    """
    This strategy don't work on this system.
    """

    def __init__(self, name, hint):
        self.name = name
        self.hint = hint

def decodict(d):
    return dict((k, v.decode('utf-8')) for k, v in d.iteritems())

class GeneralWriterStrategy(object):

    description = 'Not shure what this does'
    name = None

    options = (template_option,)

    hint = 'Something is wrong. This writer is not supposed to fail.'

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
        destination.write( (template.decode('utf-8') %
                            decodict(parts)).encode('utf-8') )

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
        return writers.get_writer_class(cls.name)()

    @classmethod
    def add_options(cls, parser):
        """
        Add options specific to this writer.
        """
        add_bool_opt, add_str_opt = util.default_option_adders(parser)
        add_str_opt('-c', '--config', help='XXX config help text..')
        add_bool_opt('-d', '--dump-parts', help='XXX dump parts help text..')
        if hasattr(cls, 'options'):
            for name, (typ, shortn, longn, hlp) in cls.options:
                if typ is str:
                    add_str_opt(shortn, longn, help=hlp)
                elif typ is bool:
                    add_bool_opt(shortn, longn, help=hlp)

class HtmlStrategy(GeneralWriterStrategy):

    description = 'HTML (docutils builtin)'
    name = 'html4css1'

    options = (template_option, stylesheets_option)

class PseudoXmlStrategy(GeneralWriterStrategy):

    description = "'pseudo xml' (docutils builtin)"
    name = 'pseudoxml'

class DocutilsXmlStrategy(GeneralWriterStrategy):

    description = 'docutils own XML (docutils built in)'
    name = 'docutils_xml'

class S5HtmlStrategy(GeneralWriterStrategy):

    description = 'Renders S5 HTML (docutils built in)'
    name = 's5_html'

class LatexStrategy(GeneralWriterStrategy):

    description = 'LaTeX (docutils built in)'
    name = 'latex2e'

    options = (template_option, stylesheets_option)

    @property
    def settings(self):
        settings = {'language': self.options.lang}
        if hasattr(self.options, 'stylesheets'):
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

    hint = 'Install TeX Live/MikTex or similar on your system'

class XeLaTeXStrategy(LatexPostProcessingStrategy):

    description = 'PDF via LaTeX and `xelatex`'

    # XXX see XXX in Latex2PDFStrategy
    program = 'xelatex'

    # encoding is implicitly unicode in XeLaTeX

    hint = 'Install XeTeX on your system (http://scripts.sil.org/XeTeX)'

class OdtStrategy(GeneralWriterStrategy):

    description = 'OpenDocument'
    options = (stylesheets_option,)

    hint = 'Install OdtWriter for Docutils in your python installation.'

    def postprocess(self, parts, template, destination):
        destination.write(parts['whole'])

    @classmethod
    def writer_object(cls):
        from odtwriter import Writer
        return Writer()

class RtfStrategy(GeneralWriterStrategy):

    description = "Microsoft's Rich Text Format ('RTF')"
    options = (stylesheets_option,)

    @classmethod
    def writer_object(cls):
        from flexirest.rtf import RtfWriter
        return RtfWriter()

# XXX Beware: the _writer_aliases dict is undocumented and marked as
# private! In theory we should find out a better way to produce this
# list, but right now I don't see any way of doing that.
# builtin_writers = dict.fromkeys(set(chain(writers._writer_aliases.keys(),
#                                           writers._writer_aliases.values())),
#                                 GeneralWriterStrategy)
# builtin_writers['latex'] = LatexStrategy
# builtin_writers['latex2e'] = LatexStrategy

# pseudo_writers = {'latex2pdf': Latex2PDFStrategy,
#                   'xelatex': XeLaTeXStrategy}

# external_writers = {'odt': OdtStrategy,
#                     'rtf': RtfStrategy}

# def functional_strategies():
#     for name, Strategy in chain(builtin_writers.items(),
#                                 pseudo_writers.items(),
#                                 external_writers.items()):
#         strategy = Strategy()
#         yield name, Strategy

possible_writers = {
    'latex': LatexStrategy,
    'xml': DocutilsXmlStrategy,
    'pdflatex': Latex2PDFStrategy,
    'xelatex': XeLaTeXStrategy,
    'odt': OdtStrategy,
    's5': S5HtmlStrategy,
    'html': HtmlStrategy,
    'pseudoxml': PseudoXmlStrategy,
    'rtf': RtfStrategy,
}

def check_writers(writers=possible_writers):
    functional = {}
    nonfunctional = {}
    for name, Strategy in writers.iteritems():
        if Strategy.isfunctional():
            functional[name] = Strategy
        else:
            nonfunctional[name] = Strategy

    return functional, nonfunctional

def from_name(name):
    """
    Create strategy object corresponding to `name`. Returns strategy
    object or raises a `NonFunctionalStrategy` exception with the
    strategy name and a hint on how to fix it.
    """
    Strategy = possible_writers[name]
    if Strategy.isfunctional():
        strategy = Strategy()
        strategy.name = name
        return strategy
    raise NonFunctionalStrategy(name, Strategy.hint)

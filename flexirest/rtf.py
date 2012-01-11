# -*- coding: utf-8 -*-

# Ref, convert RTF to HTML via AbiWord (verification purpose):
# $ abiword --to=outfile.html abiword.rtf

import re

from collections import deque
from cStringIO import StringIO

from docutils import nodes, utils, writers, languages
import PyRTF as rtf

__docformat__ = 'reStructuredText'

class RtfWriter(writers.Writer):
    """
    Writer class to write to RFT using `PyRTF`.
    """

    supported = ('rtf',)
    """Format this writer will write."""

    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = RtfTranslator

    def translate(self):
        visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()

class RtfTranslator(nodes.NodeVisitor):
    """
    Translate to RTF.
    """

    words_and_spaces = re.compile(r'\S+| +|\n')

    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.settings = settings = document.settings
        lcode = settings.language_code
        class Reporter(object):
            def warning(self, msg):
                print('docutils warning: %s' % msg)
        self.language = languages.get_language(lcode, Reporter())
        self.section_level = 0

        self.doc = rtf.Document()
        self.style = self.doc.StyleSheet
        #self.head = rtf.Section()
        self.body = rtf.Section()
        #self.doc.Sections.append(self.head)
        self.doc.Sections.append(self.body)
        self.next_style = 'Normal'

    def astext(self):
        """
        'Renders' the contents.
        """
        out = StringIO()
        rtf.Renderer().Write(self.doc, out)
        return out.getvalue()

    def build_paragraph(self, text, style='Normal'):
        para = rtf.Paragraph(getattr(self.style.ParagraphStyles,
                                     style))
        para.append(text)
        return para

    def add_paragraph(self, section, text, style='Normal'):
        section.append(self.build_paragraph(text, style))


    def nop_visit(self, node):
        pass

    def visit_Text(self, node):
        print('visit_Text: adding text %s' % node.astext().encode('utf-8'))

        p = self.add_paragraph(self.body,
                               node.astext().encode('utf-8'),
                               self.next_style)
        self.next_style = 'Normal'

    depart_Text = nop_visit

    visit_document = nop_visit
    depart_document = nop_visit

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    def visit_title(self, node):
        """
        Tricky and boring one. TODO: think of a nicer way of
        implementing this.
        """
        if isinstance(node.parent, nodes.topic):
            #self.body.append(self.defs['topic-title'][0])
            pass # topic-title
        elif isinstance(node.parent, nodes.sidebar):
            #self.body.append(self.defs['sidebar-title'][0])
            pass # "sidebar-title" (what was that again..?)
        elif isinstance(node.parent, nodes.admonition):
            #self.body.append('.IP "')
            pass # admonition
        elif self.section_level == 0:
            # Document title
            # raise nodes.SkipNode
            self.next_style = 'Heading1'
            print('visits main title: %s' % node.astext())
        elif self.section_level > 0:
            pass

        # txt = node.astext().upper()
        # mark = len(txt)*'=' + ' '
        # self.head.extend((mark, txt, mark, '\n'))

    def depart_title(self, node):
        if self.section_level == 0:
            self.out = self.body

    visit_paragraph = nop_visit
    depart_paragraph = nop_visit

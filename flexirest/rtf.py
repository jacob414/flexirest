# -*- coding: utf-8 -*-

import re

from collections import deque
from cStringIO import StringIO

from docutils import nodes, utils, writers, languages
import PyRTF

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
        self.language = languages.get_language(lcode)
        self.section_level = 0

        self.topsections = deque()
        self.topsections.append(PyRTF.Section())

        # POC
        self.head = []
        self.body = []

    def write_at_end(self, obj):
        self.topsections[-1].append(obj)

    def astext(self):
        """
        'Renders' the contents.
        """
        doc = PyRTF.Document()
        for section in self.topsections:
            doc.Sections.append(section)

        out = StringIO()
        PyRTF.Renderer().Write(doc, out)
        return out.getvalue()

    def nop_visit(self, node):
        pass

    def visit_Text(self, node):
        self.write_at_end(node.astext().encode('utf-8'))

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
            self.topsections[0].append('== ')
        elif self.section_level > 0:
            pass

        txt = node.astext().upper()
        mark = len(txt)*'=' + ' '
        self.head.extend((mark, txt, mark, '\n'))

    def depart_title(self, node):
        if self.section_level == 0:
            self.topsections[0]

    depart_title = nop_visit

    def visit_paragraph(self, node):
        self.body.append('\nP:')

    depart_paragraph = nop_visit

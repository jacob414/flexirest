__docformat__ = 'reStructuredText'

from docutils.core import publish_parts

import PyRTF
from flexirest import rtf

from flexirest.test.support import MINIMAL_FIXTURE

def test_sanity():
    parts = publish_parts(source=MINIMAL_FIXTURE,
                          writer=rtf.RtfWriter() )
    print( parts['whole'] )

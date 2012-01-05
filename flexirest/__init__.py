__docformat__ = 'reStructuredText'

SHORT_NAME='flexirest'
CMDLINE_DESC = 'The flexible and friendly reStructuredText utility'
VERSION = '0.9dev'
URL = 'http://www.aspektratio.net/flexirest'
AUTHOR = 'Jacob Oscarson'
EMAIL = 'jacob@plexical.com'
SHORT_DESC = CMDLINE_DESC
CMDLINE_USAGE = 'flexirest <options>'
INFO = """Flexirest
Flexible and friendly reStructuredText renderer
Version %s

Usage: flexirest <writer name> [options] [infile] [outfile]
"""
STATUS = """The following writers are functional in your installation:
{{for line in functional}}
  {{line}}
{{endfor}}

The following writers are not functional in your installation:
{{for line in nonfunctional}}
  {{line}}
{{endfor}}
"""

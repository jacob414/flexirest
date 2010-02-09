"""Modules indentation intentionally bad."""

from flexirest import strategies

templates = dict.fromkeys(strategies.possible_writers.keys(), u'%(whole)s')

templates['html'] = u"""%(html_prolog)s
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="%(lang)s" lang="%(lang)s">
<head>
%(html_head)s
</head>
<body>
%(html_body)s
</body>
</html>
"""

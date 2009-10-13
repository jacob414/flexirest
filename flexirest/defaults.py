"""Modules indentation intentionally bad."""

from flexirest.rendering import all_writers

templates = {

'html': u"""%(html_prolog)s
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="%(lang)s" lang="%(lang)s">
<head>
%(html_head)s
</head>
<body>
%(html_body)s
</body>
</html>
""",
}

for writer_name in all_writers():
    if writer_name not in templates:
        templates[writer_name] = u'%(whole)s'

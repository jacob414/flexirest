"""Modules indentation intentionally bad."""

from flexirest.rendering import all_writers

templates = {

'html': u"""%(html_prolog)s
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
%(html_head)s
</head>
<body>
%(html_body)s
</body>
</html_body>
""",
}

for writer_name in all_writers():
    templates[writer_name] = u's%(whole)s'

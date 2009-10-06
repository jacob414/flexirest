"""Modules indentation intentionally bad."""

# XXX Very rough for now
latex_template = u"""
%(head_prefix)s

%(head)s

%(body_prefix)s

%(body)s

%(body_suffix)s
"""

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

'latex': latex_template,
'latex2e': latex_template,
'newlatex2e': latex_template,


}

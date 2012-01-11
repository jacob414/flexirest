from __future__ import with_statement

from flexirest.io import TempDirectory

import os
import tempfile
import subprocess
import shutil

def run_program(program, source, styles=()):
    with TempDirectory('flexirest-') as tmpdir:
        for sty in styles:
            tmpdir.copy(sty)

        tmpdir.put('texsource.tex', source.encode('utf-8'))

        last_aux = None

        for run in range(5): # XXX 5 hardcoded
            returncode = subprocess.call([program,
                                          '-halt-on-error',
                                          '-no-shell-escape',
                                          tmpdir.newpath('texsource.tex')],
                                         stdin=open(os.devnull, 'r'),
                                         stdout=open(os.devnull, 'w'),
                                         stderr=subprocess.STDOUT,
                                         close_fds=True,
                                         shell=False,
                                         cwd=tmpdir.path,
                                         env=os.environ)
            if returncode != 0:
                raise ValueError(tmpdir.open('texsource.log', 'r').read())

            aux = tmpdir.open('texsource.aux', 'r').read()
            if aux == last_aux:
                return tmpdir.open('texsource.pdf', 'r').read()
            last_aux = aux

        raise ValueError("'%s' didn't stabilize" % program)

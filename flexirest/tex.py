from __future__ import with_statement

import os
import tempfile
import subprocess
import shutil

def latex2pdf(source, styles=()):
    tmpdir = tempfile.mkdtemp(prefix='flexirest-')
    tmpfile = lambda name: os.path.join(tmpdir, name)

    try:
        for sty in styles:
            shutil.copy(sty, tmpdir)

        srcpath = tmpfile('texsource.tex')
        with open(srcpath, 'w') as fp:
            fp.write(source.encode('utf-8'))

        last_aux = None

        for run in range(5): # XXX 5 hardcoded
            proc = subprocess.Popen(['pdflatex',  # XXX hardcoded
                                     '-interaction=batchmode',
                                     '-halt-on-error',
                                     '-no-shell-escape',
                                     srcpath],
                                    stdin=open(os.devnull, 'r'),
                                    stdout=open(os.devnull, 'w'),
                                    stderr=subprocess.STDOUT,
                                    close_fds=True,
                                    shell=False,
                                    cwd=tmpdir,
                                    env={'PATH': os.getenv('PATH')})
            proc.wait()
            if proc.returncode != 0:
                raise ValueError(open(tmpfile('texsource.log'), 'r').read())

            aux = open(tmpfile('texsource.aux'), 'r').read()
            if aux == last_aux:
                return open(tmpfile('texsource.pdf'), 'r').read()
            last_aux = aux

        raise ValueError("pdflatex didn't stabilize")
    finally:
        shutil.rmtree(tmpdir)

from __future__ import with_statement

import os

testfiles = []

def create_testfile(path, contents):
    with open(path, 'w') as fp:
        fp.write(contents)
    testfiles.append(path)

def clean_testfiles():
    for path in testfiles:
        os.unlink(path)
        testfiles.remove(path)


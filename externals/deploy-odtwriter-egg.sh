#!/bin/sh

# XXX Just a proof-of-concept, this really ought to be a buildout task
# XXX of some kind

FLEXIREST_REPO=~/src/flexirest
SANDBOX=~/src/ext/docutils-sandbox-svn

cd $SANDBOX/OpenDocument
python setup.py sdist
cd $SANDBOX/OpenDocument/dist/
tar zxf odtwriter-1.3d.tar.gz
cd $SANDBOX/OpenDocument/dist/odtwriter-1.3d
patch -p0 < $FLEXIREST_REPO/externals/odtwriter-eggpatch.diff
python setup.py bdist_egg
rsync -r dist/odtwriter-1.3d-py2.6.egg flexisite:~/public_html/flexirest/dist/

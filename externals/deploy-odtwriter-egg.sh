#!/bin/sh

# XXX Just a proof-of-concept, this really ought to be a buildout task
# XXX of some kind

rm -rf odtwriter-svn
svn co svn://svn.berlios.de/docutils/trunk/sandbox/OpenDocument odtwriter-svn
cd odtwriter-svn
patch -p0 < ../odtwriter-eggpatch.diff
python setup.py bdist_egg
python2.5 setup.py bdist_egg
rsync -r dist/*.egg flexisite:~/public_html/flexirest/dist/

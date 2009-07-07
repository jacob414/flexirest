import os
from setuptools import setup, find_packages

from flexirest import meta

packages = [meta.SHORT_NAME]

setup(name=meta.SHORT_NAME,
      packages=packages,
      version=meta.VERSION,
      author=meta.AUTHOR,
      author_email=meta.EMAIL,
      url=meta.URL,
      description=meta.SHORT_DESC,
      entry_points = {
          'console_scripts': (
              'frest = flexirest.main:commandline',
              )
          },
      classifiers = [
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Multimedia :: Sound/Audio',
          'Framework :: Buildout'
          ],
      license='GNU LGPL',
      test_suite='nose.collector')

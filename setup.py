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
      long_description=open('docs/introduction.txt', 'r').read(),
      install_requires=['docutils'],
      entry_points = {
          'console_scripts': (
              'flexirest = flexirest.main:commandline',
              )
          },
      classifiers = [
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Environment :: Console',
          'Topic :: Documentation',
          'Topic :: Software Development :: Documentation',
          'Topic :: Text Processing :: Markup',
          ],
      license='GNU LGPL',
      test_suite='nose.collector')


# -*- coding: utf-8 -*-
"""pavement.py -- pavement for Flexirest.

Copyright 2011 Jacob Oscarson. See LICENCE for permissions.
"""
import os
import sys

from paver.easy import *
from paver.setuputils import setup

try:
    import flexirest
except ImportError:
    sys.path.append('.')
    import flexirest

setup(
    name=flexirest.SHORT_NAME,
    packages=(flexirest.SHORT_NAME),
    version='0.9dev',
    author=flexirest.AUTHOR,
    author_email=flexirest.EMAIL,
    install_requires=open(os.path.join('deps',
                                       'requirements.txt')).readlines()
)

@task
def readme():
    "Builds top-level README.rst"

@task
def virtualenv():
    "Prepares a checked out directory for development"
    if not os.path.exists(os.path.join('bin', 'pip')):
        sys.path.insert(0, os.path.join('deps', 'virtualenv.zip'))
        import virtualenv
        virtualenv.create_environment('.')
    else:
        print('Virtualenv already set up')

@needs('virtualenv')
@task
def env():
    "Ensure virtualenv exists and is up to date"
    sh('./bin/pip install -r deps/requirements.txt')
    sh('./bin/pip install -r deps/development.txt')

@task
def clean():
    "Remove everything created by the build process"
    path('bin').rmtree()
    path('lib').rmtree()
    path('include').rmtree()

import pytest

import os, sys, imp, errno

from StringIO import StringIO

from flexirest.util import substitute

import flexirest
from flexirest import main, rendering
from flexirest.test import support
from flexirest.test.support import LineCapture

def test_info():
    """
    Tests output of running without parameters
    """
    io = support.CapturingIo()
    rc = main.commandline(args=(), io=io)
    assert rc == 0
    assert io.message.startswith('Flexirest')

def test_version():
    """
    Tests the output of the 'version' command
    """
    def check_version(variant):
        io = support.CapturingIo()
        retc = main.commandline(args=[variant,], io=io)
        assert retc == 0
        assert io.msglines == [flexirest.VERSION, '']

    for variant in ('-v', '--version', 'version'):
        yield check_version, variant

expected_status_start = (
"""The following writers are functional in your installation:
    html          HTML (docutils builtin)
    latex         LaTeX (docutils built in)""")

def test_show_status():
    """
    Tests the output of the 'status' command
    """
    def check_status(variant):
        io = support.CapturingIo()
        rc = main.commandline(args=[variant], io=io)
        assert rc == 0
        assert io.message.startswith(expected_status_start)

    for variant in ('status', 'st'):
        yield check_status, variant

def test_dump_parts():
    io = support.CapturingIo()
    io.source = support.get_minimal_fixture()
    rc = main.commandline(['latex', '--dump-parts'], io=io)
    # XXX sanity check only
    assert io.msglines[0].startswith("Parts created by the docutils")

def test_explicit_confmodule_not_found_raises():
    with pytest.raises(ImportError):
        main.commandline(['latex', '--config=notamodule'], io=support.NullIo())

def test_no_default_confmodule_noraise():
    io = support.CapturingIo()
    io.source = support.get_minimal_fixture()
    main.commandline([], io=io)

def test_bad_writer_nice_error():
    io = support.CapturingIo()
    rc = main.commandline(['bad_writer'], io=io)
    assert rc, errno.EINVAL
    assert (io.errlines ==
                  ["flexirest: 'bad_writer' is not a valid writer", ''])


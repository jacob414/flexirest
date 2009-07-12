import os
import sys
import imp

from flexirest import main, meta
from nose.tools import assert_equals, assert_true, with_setup, raises

from flexirest.tests.support import Capturer

def test_help():
    outp = Capturer()
    old_stdout = sys.stdout
    try:
        sys.stdout = outp
        retc = main.commandline(args=['--help'])
    except SystemExit, e:
        assert_equals(e.code, 0)
    finally:
        sys.stdout = old_stdout
        _help = outp.lines[0].split(os.linesep)
        assert_equals(_help[0], 'Usage: flexirest <options>')
        assert_true(_help[5].endswith('show this help message and exit'))

def test_version():
    outp = Capturer()
    retc = main.commandline(args=['--version',], console=outp)
    assert_equals(retc, 0)
    assert_equals(outp.lines, ["flexirest version '%s'" % meta.VERSION])

old_main_import = None
old_main_regroles = None
fake_main_import = None

reg_canonical_roles = {}

def role_one():
    pass

def role_two():
    pass

def role_three():
    pass

def fake_import(name):
    mod = imp.new_module(name)
    mod.role_one = role_one
    mod.role_two = role_two
    mod.role_three = role_three
    return mod

def register_canonical_role(name, func):
    reg_canonical_roles[name] = func

def monkeypatch_main():
    old_main_import = main._import
    old_main_regroles = main.roles.register_canonical_role
    main.roles.register_canonical_role = register_canonical_role
    main._import = fake_import

def unpatch_main():
    main._import = old_main_import
    main.roles.register_canonical_role = old_main_regroles

@raises(ImportError)
def test_main_default_roles_raises():
    main.commandline(['--roles', 'notamodule'])

@with_setup(monkeypatch_main, unpatch_main)
def test_roles():
    main.commandline(['--roles', 'the-rolename'])

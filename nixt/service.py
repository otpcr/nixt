# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105,W0212


"service"


import getpass
import os
import pwd
import sys


from .main    import forever, init, scan, wrap
from .modules import face
from .persist import modname, pidfile, pidname
from .runtime import Errors


def errors():
    "print errors."
    for err in Errors.errors:
        for line in err:
            print(line)


def privileges(username):
    "privileges."
    pwnam2 = pwd.getpwnam(username)
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


def main():
    "main"
    privileges(getpass.getuser())
    pidfile(pidname())
    scan(face)
    init(face)
    forever()


if __name__ == "__main__":
    wrap(main)
    errors()

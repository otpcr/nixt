# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105,W0212,W0718


"daemon"


import getpass
import os
import pwd
import sys


from .main    import forever, scan, init, wrap
from .modules import face
from .persist import modname, pidfile, pidname
from .runtime import Errors


def daemon(verbose=False):
    "switch to background."
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    os.nice(10)


def errors():
    "print errors."
    for error in Errors.errors:
        for line in error:
            print(line)


def privileges(username):
    "privileges."
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def main():
    "main"
    daemon(True)
    privileges(getpass.getuser())
    pidfile(pidname())
    scan(face)
    init(face)
    forever()


if __name__ == "__main__":
    wrap(main)
    errors()

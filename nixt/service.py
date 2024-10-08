# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105


"service"


import getpass
import os
import pwd


from .command import boot
from .modules import face as faced
from .persist import pidfile, pidname
from .runtime import Errors, forever, init, wrap


if os.path.exists("mods"):
    from mods import face as MODS
else:
    MODS = None    


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
    boot(MODS)
    init(faced)
    forever()


if __name__ == "__main__":
    wrap(main)
    errors()

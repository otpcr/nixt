# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105,W0611


"cli"


import os
import sys


from nixt.main    import Config, command, scan
from nixt.modules import face
from nixt.object  import parse
from nixt.persist import modname
from nixt.runtime import Client, Errors, Event


cfg = Config()


class CLI(Client):

    "CLI"


    def raw(self, txt):
        "print text."
        print(txt)


def errors():
    "print errors."
    for error in Errors.errors:
        for line in error:
            print(line)


def main():
    "main"
    parse(cfg, " ".join(sys.argv[1:]))
    scan(face)
    cli = CLI()
    evt = Event()
    evt.txt = cfg.txt
    command(cli, evt)
    evt.wait()


if __name__ == "__main__":
    main()
    errors()

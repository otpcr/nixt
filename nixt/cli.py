# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105,W0611


"cli"


import os
import sys


from .broker  import Broker
from .command import command, parse
from .main    import boot
from .runtime import Client, Config, Errors, Event


cfg = Config()


if os.path.exists("mods"):
    from mods import face as MODS
else:
    MODS = None    


class CLI(Client):

    "CLI"

    def __init__(self):
        Client.__init__(self)
        Broker.add(self)
        self.register("event", command)

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
    boot(MODS)
    cli = CLI()
    evt = Event()
    evt.txt = cfg.txt
    command(cli, evt)
    evt.wait()


if __name__ == "__main__":
    main()
    errors()

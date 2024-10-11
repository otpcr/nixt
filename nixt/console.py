# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105,W0212,W0718


"console"


import os
import readline
import sys
import termios
import time


from nixt.main    import NAME, Config, command, forever, scan, init
from nixt.modules import face
from nixt.object  import parse
from nixt.persist import modname
from nixt.runtime import Client, Errors, Event
from nixt.runtime import later


Cfg = Config()


class Console(Client):

    "Console"

    def __init__(self):
        Client.__init__(self)
        self.register("event", command)

    def callback(self, evt):
        "wait for result."
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        "poll console and create event."
        evt = Event()
        evt.txt = input("> ")
        return evt

    def raw(self, txt):
        "print text."
        print(txt)


def banner():
    "show banner."
    tme = time.ctime(time.time()).replace("  ", " ")
    print(f"{NAME.upper()} since {tme}")


def errors():
    "print errors."
    for error in Errors.errors:
        for line in error:
            print(line)


def wrap(func):
    "reset console."
    old2 = None
    try:
        old2 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    except Exception as ex:
        later(ex)
    finally:
        if old2:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old2)


def main():
    "main"
    parse(Cfg, " ".join(sys.argv[1:]))
    scan(face)
    if "v" in Cfg.opts:
        readline.redisplay()
        banner()
        face.irc.output = print
    if "i" in Cfg.opts:
        for _mod, thr in init(modr):
            if "w" in Cfg.opts:
                thr.join()
    csl = Console()
    csl.start()
    forever()


if __name__ == "__main__":
    wrap(main)
    errors()

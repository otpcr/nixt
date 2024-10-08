# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105,W0718


"console"


import os
import readline
import sys
import termios
import time


from .broker  import Broker
from .command import command, parse
from .main    import NAME, boot, forever, init
from .runtime import Client, Config, Errors, Event, later


cfg = Config()


if os.path.exists("mods"):
    from mods import face as MODS
else:
    MODS = None    


class Console(Client):

    "Console"

    def __init__(self):
        Client.__init__(self)
        Broker.add(self)
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
    if not Errors.errors and "v" in cfg.opts:
        print("no errors")


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
    readline.redisplay()
    parse(cfg, " ".join(sys.argv[1:]))
    boot(MODS)
    if "v" in cfg.opts:
        banner()
        if MODS:
            MODS.irc.output = print
    if "i" in cfg.opts:
        for _mod, thr in init(MODS):
            if "w" in cfg.opts:
                thr.join()
    csl = Console()
    csl.start()
    forever()


if __name__ == "__main__":
    wrap(main)
    errors()
#!/usr/bin/env python3
# This file is placed in the Public Domain.
# pylint: disable=C0413


"cli"


import getpass
import os
import sys
import termios
import time
import _thread


from nixt.command import Commands, Config, command, parse, scanner
from nixt.modules import face
from nixt.runtime import NAME, Client, Errors, Event, later, launch


cfg = Config()


class CLI(Client):

    "CLI"

    def raw(self, txt):
        "print text."
        print(txt)


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


"utilitites"


def banner():
    "show banner."
    tme = time.ctime(time.time()).replace("  ", " ")
    print(f"{NAME.upper()} since {tme}")


def cprint(txt):
    print(txt)
    sys.stdout.flush()


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
    if not Errors.errors and "v" in cfg.opts:
        print("no errors")


def forever():
    "it doesn't stop, until ctrl-c"
    while True:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def init(*pkgs):
    "run the init function in modules."
    mods = []
    for pkg in pkgs:
        for modname in dir(pkg):
            if modname.startswith("__"):
                continue
            modi = getattr(pkg, modname)
            if "init" not in dir(modi):
                continue
            thr = launch(modi.init)
            mods.append((modi, thr))
    return mods


def opts(options):
    for opt in options:
        if opt in cfg.opts:
            return True
    return False


def privileges(username):
    "privileges."
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


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
    parse(cfg, " ".join(sys.argv[1:]))
    if opts("d"):
        daemon()
    if opts("ds"):
        privileges(getuser.getpass())
        pidfile(pidname())
    if opts("v"):
        banner()
        face.irc.output = print
    if opts("i"):
        for _mod, thr in init(face):
            if opts("w"):
                thr.join()
    scanner(face)
    if opts("c"):
        csl = Console()
        csl.start()
    if opts("dsc"):
        forever()
        return
    cli = CLI()
    evt = Event()
    evt.txt = cfg.txt
    command(cli, evt)
    evt.wait()


if __name__ == "__main__":
    wrap(main)
    errors()

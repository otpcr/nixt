# This file is placed in the Public Domain.
# pylint: disable=C0415,W0105


"main"


import getpass
import os
import pathlib
import pwd
import readline
import sys
import termios
import time


from .clients import Client
from .command import Commands, command, md5sum, parse, scan
from .loggers import loglevel
from .objects import dumps
from .persist import Workdir, pidname
from .runtime import Config, Event, errors, exceptions, forever, later


cfg = Config()
p   = os.path.join


Workdir.wdr = os.path.expanduser(f"~/.{Config.name}")


"cli"


class CLI(Client):

    """ Command Line Interface """

    def raw(self, txt):
        """ echo raw text. """
        print(txt.encode('utf-8', 'replace').decode("utf-8"))
        sys.stdout.flush()

    def say(self, _channel, txt):
        """ relay to raw. """
        self.raw(txt)


class Console(CLI):

    """ Console """

    def announce(self, txt):
        """ disable announce. """

    def callback(self, evt):
        """ wait for callback to finish. """
        CLI.callback(self, evt)
        evt.wait()

    def poll(self):
        """ poll for event. """
        evt = Event()
        evt.orig = repr(self)
        evt.txt = input("> ")
        evt.type = "command"
        return evt


"utilities"


def banner():
    """ show banner. """
    tme = time.ctime(time.time()).replace("  ", " ")
    print(f"{Config.name.upper()} since {tme}")


def check(txt):
    """ check for options. """
    args = sys.argv[1:]
    for arg in args:
        if not arg.startswith("-"):
            continue
        for char in txt:
            if char in arg:
                return True
    return False


def daemon(verbose=False):
    """ run in the background. """
    pid = os.fork()
    if pid != 0:
        sys.exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        sys.exit(0)
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


def pidfile(filename):
    """ write the pid to a file. """
    if os.path.exists(filename):
        os.unlink(filename)
    path = pathlib.Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges():
    """ drop privileges. """
    pwnam = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


"scripts"


def background():
    """ run in the background. """
    daemon(True)
    privileges()
    pidfile(pidname(Config.name))
    from . import modules as MODS
    scan(MODS, init=True)
    forever()


def console():
    """ run console. """
    parse(cfg, " ".join(sys.argv[1:]))
    Config.dis  = cfg.sets.dis or Config.dis
    Config.mods = cfg.sets.mods or Config.mods
    if "v" in cfg.opts:
        banner()
        loglevel(Config.level)
    from . import modules as MODS
    for _mod, thr in scan(MODS, init="i" in cfg.opts, disable=Config.dis):
        #if "v" in cfg.opts and "output" in dir(mod):
        #    mod.output = print
        if thr and "w" in cfg.opts:
            thr.join()
    csl = Console()
    csl.start()
    forever()


def control():
    """ daemon control. """
    if len(sys.argv) == 1:
        return
    Commands.add(md5)
    Commands.add(srv)
    parse(cfg, " ".join(sys.argv[1:]))
    cfg.dis = cfg.sets.dis or cfg.dis
    csl = CLI()
    if "v" in cfg.opts:
        loglevel(Config.level)
    from . import modules as MODS
    scan(MODS, disable=cfg.dis)
    evt = Event()
    evt.orig = repr(csl)
    evt.type = "command"
    evt.txt = cfg.otxt
    command(evt)
    #evt.wait()


def service():
    """ run as service. """
    privileges()
    pidfile(pidname(Config.name))
    from . import modules as MODS
    scan(MODS, init=True)
    forever()


"commands"


def md5(event):
    """ command to create md5 sum dictionary. """
    if not event.args:
        event.reply("md5 <path>")
        return
    path = event.args[0]
    res = {}
    for fnm in os.listdir(path):
        if fnm.startswith("__"):
            continue
        if not fnm.endswith(".py"):
            continue
        with open(f"{path}/{fnm}", "r", encoding="utf-8") as file:
            data = file.read()
            res[fnm[:-3]] = md5sum(data)
    event.reply("# This file is placed in the Public Domain.")
    event.reply("")
    event.reply('"md5sums"')
    event.reply("")
    event.reply(f"MD5 = {dumps(res, indent=4, sort_keys=True)}")


def srv(event):
    """ command to create service file. """
    name = getpass.getuser()
    event.reply(TXT % (Config.name.upper(), name, name, name, Config.name))


"runtime"


def wrap(func):
    """ wrapper to restore console. """
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    except exceptions as exc:
        later(exc)
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)
    for line in errors():
        print(line)


def wrapped():
    """ wrap main. """
    wrap(main)


def wraps():
    """ wrap service. """
    wrap(service)


def main():
    """ main """
    if check("c"):
        readline.redisplay()
        wrap(console)
    elif check("d"):
        background()
    elif check("s"):
        wrap(service)
    else:
        control()


TXT = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""


if __name__ == "__main__":
    main()

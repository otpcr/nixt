# This file is placed in the Public Domain.
# pylint: disable=C,W0611


"create service file"


import getpass


from nixt.main import Commands


NAME = Commands.__module__.split(".", maxsplit=2)[-2]
TXT = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%ss

[Install]
WantedBy=multi-user.target"""


def srv(event):
    name  = getpass.getuser()
    event.reply(TXT % (NAME.upper(), name, name, name, NAME))


def register():
    Commands.add(srv)

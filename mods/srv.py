# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105,W0611


"create service file"


import getpass


from nixt.runtime import NAME


from .command import Commands


def register():
    "register commands."
    Commands.add(srv)


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
    "create service file (pipx)."
    name  = getpass.getuser()
    event.reply(TXT % (NAME.upper(), name, name, name, NAME))

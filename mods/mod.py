# This file is placed in the Public Domain.
# pylint: disable=C


"show available modules."


import os


from nixt.runtime import Commands


def mod(event):
    path = os.path.dirname(__file__)
    mods = []
    for mdd in os.listdir(path):
        if mdd == "face.py":
            continue
        if mdd.startswith("__"):
            continue
        if mdd.endswith("~"):
            continue
        mods.append(mdd[:-3])
    event.reply(",".join(sorted(mods)))


def register():
    Commands.add(mod)

# This file is placed in the Public Domain.


""" show list of commands """


from nixt.command import Commands


def cmd(event):
    """ available commands """
    event.reply(",".join(sorted(Commands.cmds.keys())))

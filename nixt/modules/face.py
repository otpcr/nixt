# This file is placed in the Public Domain.
# pylint: disable=W0611
# ruff: noqa: F401


"interface"


MODS = (
    'cmd',
    'err',
    'flt',
    'fnd',
    'irc',
    'log',
    'mbx',
    'mdl',
    'mod',
    'req',
    'rss',
    'rst',
    'slg',
    'tdo',
    'thr',
    'tmr',
    'udp',
    'upt',
    'wsd'
)


def __dir__():
    return MODS

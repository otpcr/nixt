# This file is placed in the Public Domain.
# pylint: disable=R,W0105,W0212,W0718,E1102


"errors"


import traceback


class Errors:

    "Errors"

    errors = []


def format(exc):
    "format an exception"
    return traceback.format_exception(
                               type(exc),
                               exc,
                               exc.__traceback__
                              )


def later(exc):
    "add an exception"
    excp = exc.with_traceback(exc.__traceback__)
    fmt = format(excp)
    if fmt not in Errors.errors:
        Errors.errors.append(fmt)


def __dir__():
    return (
        'Errors',
        'format',
        'later'
    )

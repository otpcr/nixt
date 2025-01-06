# This file is placed in the Public Domain.


"errors"


import traceback


class Error:

    errors = []

    @staticmethod
    def format(exc):
        return traceback.format_exception(
            type(exc),
            exc,
            exc.__traceback__
        )


def errors():
    for err in Error.errors:
        for line in err:
            yield line


def later(exc):
    excp = exc.with_traceback(exc.__traceback__)
    fmt = Error.format(excp)
    if fmt not in Error.errors:
        Error.errors.append(fmt)

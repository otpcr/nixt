# This file is placed in the Public Domain.
# pylint: disable=C,W0718,E0402


"workers"


import psutil
import queue
import threading
import time
import _thread


from .command import command
from .error import later


class Worker(threading.Thread):

    def __init__(self, thrname="", daemon=False):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self.name = thrname
        self.queue = queue.Queue()
        self.starttime = time.time()

    def run(self):
        while True:
            try:
                bot, evt = self.queue.get()
                if evt is None:
                    break
                command(bot, evt)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()
            except Exception as ex:
                later(ex)


class Pool:

    laters = []
    pool   = []

    @staticmethod
    def dispatch(bot, evt):
        for worker in Pool.pool:
            if worker.queue.qsize() == 0:
                worker.queue.put((bot, evt))
                return True
        return False

    @staticmethod
    def put(bot, evt):
        if not Pool.pool:
            Pool.start()
        if not Pool.dispatch(bot, evt):
            Pool.laters.append((bot, evt))
            for evt in Pool.laters:
                if Pool.dispatch(bot, evt):
                    return True
        return False

    @staticmethod
    def start():
        for _nr in range(psutil.cpu_count()):
            Pool.pool.append(Worker())
        for worker in Pool.pool:
            worker.start()


def __dir__():
    return (
        'Pool',
        'Worker'
    )

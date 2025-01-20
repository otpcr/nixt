# This file is placed in the Public Domain.


"cache"


class Cache:

    """ Cache """

    objs = {}

    @staticmethod
    def add(path, obj):
        """ add object to cache. """
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        """ get object from cache. """
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher):
        """ match typed objects. """
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


class Fleet:

    """ Fleet. """

    bots = {}

    @staticmethod
    def add(bot):
        """ add to fleet."""
        Fleet.bots[repr(bot)] = bot

    @staticmethod
    def announce(txt):
        """ announce on fleet."""
        for bot in Fleet.bots:
            bot.announce(txt)

    @staticmethod
    def get(orig):
        """get by origin."""
        return Fleet.bots.get(orig, None)

    @staticmethod
    def say(orig, channel, txt):
        """ say text on channel on specific bot."""
        bot = Fleet.bots.get(orig, None)
        if bot:
            bot.say(channel, txt)


def __dir__():
    return (
        'Cache',
        'Fleet'
    )

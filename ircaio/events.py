from functools import partial
from asyncio import coroutine, iscoroutine, wait
from attrdict import AttrDict

class Events(object):

    __events__ = {}

    def __add_event__(self, event:str, fn):
        if not event in self.__events__:
            self.__events__[event] = []
        self.__events__[event].append(fn)

    def on(self, event:str):
        '''
        >>> event = Events()
        >>> type(event.on('PRIVMSG'))
        <class 'function'>
        >>> @event.on('PRIVMSG')
        ... def privmsg(bot, kwargs):
        ...     if kwargs.nick != bot.nick and kwargs.nick != kwargs.target:
        ...        bot.send('PRIVMSG', target=kwargs.target, message='{}: {}'.format(kwargs.nick, kwargs.message))
        '''
        def hook(fn):
            self.__add_event__(event, fn if iscoroutine(fn) else coroutine(fn))
            return fn
        return hook

    @coroutine
    def trigger(self, protocol, event:str, kwargs):
        '''
        Example
        >>> yield from event.trigger(bot, 'PRIVMSG', {
        ...     'target':"#linux-cn",
        ...     'nick':"quininer",
        ...     'message':"Hello world."
        ... })
        '''
        if not event in self.event.__events__:
            return
        fns = [partial(fn, protocol)(AttrDict(kwargs)) for fn in self.__events__[event]]

        protocol.log.info('trigger', self.__events__[event], kwargs)

        if bool(fns):
            yield from wait(fns)

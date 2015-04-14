from functools import partial
from asyncio import coroutine, iscoroutine, wait

class Events(object):

    __partials__ = {}

    def __add_event__(self, event:str, fn):
        self.__partials__[event].append(fn if iscoroutine(fn) else coroutine(fn))

    def on(self, event:str):
        def hook(fn):
            self.__add_event__(event, fn)
        return hook

    @coroutine
    def trigger(self, event, **kwargs):
        fns = [partial(fn, self.irc)(**kwargs) for fn in self.__partials__[event]]
        if bool(fns):
            yield from wait(fns)

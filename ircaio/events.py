from functools import wraps, partial

class Events(object):

    __partials__ = {}

    def __add_event__(self, event:str, fn):
        #XXX
        self.__partials__[event].append(fn)

    def on(self, event:str):
        def decorator(fn):
            self.__add_event__(event, fn)
        return decorator

from functools import wraps, partial

class Events(object):

    __partials__ = {}

    def __add_event__(self, event:str, fn, args):
        self.__partials__[event].append(partial(fn, args))

    def on(self, event:str):
        def decorator(fn):
            @wraps(fn)
            def fn_wrap(xself):
                self.__add_event__(event, fn, xself)
                return fn
            return fn_wrap
        return decorator

#!/usr/bin/env python
# encoding: utf-8

import asyncio
from .module import module

class main(module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @asyncio.coroutine
    def join(self, kwargs):
        if kwargs.nick != self.bot.nick:
            self.send('PRIVMSG', target=kwarg.target, message='welcome to {}, {}!'.format(kwargs.target, kwargs.nick))

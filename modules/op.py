#!/usr/bin/env python
# encoding: utf-8

import asyncio
from .module import module

class main(module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = {
            'get':self.__get
        }

    @asyncio.coroutine
    def join(self, kwargs):
        if kwargs.nick == self.bot.nick:
            self.send('CHANNELMODE', channel=kwargs.channel, modes='+o')

    @asyncio.coroutine
    def __get(self, kwargs):
        modes = {
            'op':"+o",
            'voice':"+v"
        }
        args = kwargs.argument.split(' ')
        if args[0].lower() == 'me':
            args[0] = kwargs.nick
        if len(args) == 2 and args[1] in modes:
            if kwargs.host == self.bot.master:
                self.send('CHANNELMODE', channel=self.bot.channel, modes=modes[args[1]], params=args[0])
            else:
                yield from self.__warning(kwargs, 'nomaster')
        else:
            yield from self.__warning(kwargs, 'unknown')

    @asyncio.coroutine
    def __warning(self, kwargs, warning):
        self.send('PRIVMSG', target=kwargs.nick, message={
            'nomaster':"You have no permission to do so since you 're not my master, maybe you need to log in first?",
            'unknown':"What do you want to do?"
        }[warning])

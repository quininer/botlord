#!/usr/bin/env python
# encoding: utf-8

import asyncio
from .module import module

class main(module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = {
            'quit':self.__quit,
            'reload':self.__reload
        }

    @asyncio.coroutine
    def made(self):
        self.send('NICK', nick=self.bot.nick)
        if bool(self.bot.password):
            self.send('PASS', password=self.bot.password)
        if bool(self.bot.realname):
            self.send('USER', user=self.bot.nick, realname=self.bot.realname)
        if bool(self.bot.channel):
            self.send('JOIN', channel=self.bot.channel)
        else:
            self.log.warning('channel is not set.')

    @asyncio.coroutine
    def ping(self, kwargs):
        self.send('PONG', message=kwargs.message)

    @asyncio.coroutine
    def command(self, kwargs):
        message = kwargs.message.split(' ', 1)
        [cmd, args] = message if len(message) > 1 else message.append(None)
        yield from self.commands[cmd](self, args, kwargs)

    @asyncio.coroutine
    def __quit(self, args, kwargs):
        if kwargs.host == self.bot.master:
            self.send('QUIT', message=args)

    @asyncio.coroutine
    def __reload(self, args, kwargs):
        pass

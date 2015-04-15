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
        if not kwargs.command in self.commands:
            return
        self.log.debug(kwargs)
        yield from self.commands[kwargs.command](kwargs)

    @asyncio.coroutine
    def __quit(self, kwargs):
        if kwargs.host == self.bot.master:
            self.send('QUIT', message=kwargs.args)
        else:
            self.send('PRIVMSG', target=kwargs.nick, message='You are not my master, without permission to do so. Maybe you need to log in?')

    @asyncio.coroutine
    def __reload(self, kwargs):
        if kwargs.host == self.bot.master:
            self.bot.load_modules()
        else:
            self.send('PRIVMSG', target=kwargs.nick, message='You are not my master, without permission to do so. Maybe you need to log in?')


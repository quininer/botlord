#!/usr/bin/env python
# encoding: utf-8

import asyncio
from module import module

class main(module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = {
            'get':self.__get,
            'drop':self.__drop,
            'enable':self.__enable,
            'disable':self.__disable
        }

    @asyncio.coroutine
    def join(self, kwargs):
        if kwargs.nick == self.bot.nick:
            self.send('PRIVMSG', target='ChanServ', message='op {}'.format(self.bot.channel))

    @asyncio.coroutine
    def __getdrop(self, kwargs, modes):
        args = kwargs.argument.split(' ')
        self.log.debug('{}, {}'.format(kwargs.argument, modes))
        if args[0].lower() == 'me':
            args[0] = kwargs.nick
        if len(args) == 2 and args[1] in modes:
            if kwargs.host == self.bot.master:
                self.send('CHANNELMODE', channel=self.bot.channel, modes=modes[args[1].lower()], params=args[0])
            else:
                yield from self.__warning(kwargs, 'nomaster')
        else:
            yield from self.__warning(kwargs, 'unknown')

    @asyncio.coroutine
    def __get(self, kwargs):
        yield from self.__getdrop(kwargs, {
            'op':"+o",
            'voice':"+v"
        })

    @asyncio.coroutine
    def __drop(self, kwargs):
        yield from self.__getdrop(kwargs, {
            'op':"-o",
            'voice':"-v"
        })

    @asyncio.coroutine
    def __endiable(self, kwargs, modes):
        self.log.debug('{}, {}'.format(kwargs.argument, modes))
        if bool(kwargs.argument):
            if kwargs.host == self.bot.master:
                self.send('CHANNELMODE', channel=self.bot.channel, modes=modes[kwargs.argument.lower()])
            else:
                yield from self.__warning(kwargs, 'nomaster')
        else:
            yield from self.__warning(kwargs, 'unknown')

    @asyncio.coroutine
    def __enable(self, kwargs):
        yield from self.__endiable(kwargs, {
            'color':'-c'
        })

    @asyncio.coroutine
    def __disable(self, kwargs):
        yield from self.__endiable(kwargs, {
            'color':'+c'
        })

    @asyncio.coroutine
    def __warning(self, kwargs, warning):
        self.send('PRIVMSG', target=kwargs.nick, message={
            'nomaster':"You have no permission to do so since you 're not my master, maybe you need to log in first?",
            'unknown':"What do you want to do?"
        }[warning])

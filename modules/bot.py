#!/usr/bin/env python
# encoding: utf-8

from .module import module

class main(module):
    def __init__(self):
        self.commands = {
            'quit':self.__quit
        }

    def made(self, bot):
        bot.send('NICK', nick=bot.nick)
        if bool(bot.password):
            bot.send('PASS', password=bot.password)
        if bool(bot.realname):
            bot.send('USER', nick=bot.nick, realname=bot.realname)
        if bool(bot.channel):
            bot.send('JOIN', channel=bot.channel)
        else:
            bot.log.warning('channel is not set.')

    def ping(self, bot, kwargs):
        bot.send('PONG', message=kwargs.message)

    def command(self, bot, kwargs):
        message = kwargs.message.split(' ', 1)
        [cmd, args] = message if len(message) > 1 else message.append(None)
        self.commands[cmd](bot, kwargs, args)

    def __quit(self, bot, kwargs, args):
        if kwargs.host == bot.master:
            bot.send('QUIT', message=args)

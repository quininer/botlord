#!/usr/bin/env python
# encoding: utf-8

import asyncio
from time import time
from .module import module

class main(module):
    messages = {}
    start = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = asyncio.Lock()
        self.commands = {
            'patrol': self.join
        }

    @asyncio.coroutine
    def join(self, kwargs):
        if kwargs.nick == self.bot.nick or 'argument' in kwargs and kwargs.argument == 'start':
            self.start = True
            self.send('PRIVMSG', target=self.bot.master.split('/')[-1], message="patrol status {}".format(self.start))
        elif 'argument' in kwargs and kwargs.argument == 'stop':
            self.start = False

    @asyncio.coroutine
    def privmsg(self, kwargs):
        if not self.start:
            return
        t = time()
        self.log.debug("[manage] p {}".format(self.lock.locked()))
        with (yield from self.lock):
            if not kwargs.host in self.messages:
                self.messages[kwargs.host] = {
                    'msg':[],
                    'black':{
                        'l':0,
                        'q':False
                    }
                }
                tt = 0.0
            else:
                tt = self.messages[kwargs.host]['msg'][-1]['time']
            self.messages[kwargs.host]['msg'].append({
                'time':t,
                'tdoa':t-tt,
                'message':kwargs.message
            })
            self.log.debug("[manage] {}, {}, {}".format(t, t-tt, kwargs.message))
            if len(self.messages[kwargs.host]['msg']) > 10:
                self.messages[kwargs.host]['msg'].pop(0)
        self.log.debug("[manage] p- {}".format(self.lock.locked()))
        yield from self.__patrol(kwargs)

    @asyncio.coroutine
    def notice(self, kwargs):
        yield from self.privmsg(kwargs)

    @asyncio.coroutine
    def __patrol(self, kwargs):
        self.log.debug("[manage] patrol {}".format(self.lock.locked()))
        with (yield from self.lock):
            black = self.messages[kwargs.host]['black']
            msgtdoas = [i['tdoa'] for i in self.messages[kwargs.host]['msg'][black['l']:]]
        self.log.debug("[manage] patrol- {}".format(self.lock.locked()))
        length = len(msgtdoas)
        self.log.debug("[manage] {}: {}, {}, {!r}".format(kwargs.host, black, length, msgtdoas))
        if bool(length) and not black['q'] and  sum(msgtdoas)/length < (black['l']+1)*7:
            self.log.debug("[manage] {} Violation!".format(kwargs.nick))
            self.messages[kwargs.host]['black']['q'] = True
            self.messages[kwargs.host]['black']['l'] += 1
            self.send('CHANNELMODE', channel=self.bot.channel, modes='+q', params=kwargs.nick)#    禁言
            s = (self.messages[kwargs.host]['black']['l']+1)*60
            self.send('PRIVMSG', target=kwargs.nick, message="Triggered a flood control rules, you will be banned for {} seconds.".format(s))
            yield from asyncio.sleep(s)
            self.send('CHANNELMODE', channel=self.bot.channel, modes='-q', params=kwargs.nick)#    解禁
            self.messages[kwargs.host]['black']['q'] = False
            yield from asyncio.sleep(10*60)
            self.messages[kwargs.host]['black']['l'] -= 1

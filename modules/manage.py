#!/usr/bin/env python
# encoding: utf-8

import asyncio
from time import time
from module import module

class main(module):
    messages = {}

    @asyncio.coroutine
    def privmsg(self, kwargs):
        t = time()
        if not kwargs in self.messages:
            self.messages[kwargs.host] = {
                'msg':[],
                'black':0
            }
            tt = 0.0
        else:
            tt = self.messages[kwargs.host]['msg'][-1]['time']
        self.messages[kwargs.host]['msg'].append({
            'time':t,
            'tdoa':t-tt,
            'message':kwargs.message
        })
        if len(self.messages[kwargs.host]['msg']) > 10:
            self.messages[kwargs.host]['msg'].pop(0)

        yield from self.__patrol(kwargs)

    @asyncio.coroutine
    def notice(self, kwargs):
        yield from self.privmsg(kwargs)

    @asyncio.coroutine
    def __patrol(self, kwargs):
        black = self.messages[kwargs.host]['black']
        msgs = map((lambda x: x['tdoa']), self.messages[kwargs.host]['msg'][black:])
#         if msgs.count(kwargs.message) >= 3:
            # self.messages[kwargs.host]['black'] += 1
        if sum(msgs)/len(list(msgs)) < (black+1)*3:
            self.messages[kwargs.host]['black'] += 1
            self.send('CHANNELMODE', channel=self.bot.channel, modes='+q', params=kwargs.nick)#    禁言
            yield from asyncio.sleep(self.messages[kwargs.host]['black']*30)
            self.send('CHANNELMODE', channel=self.bot.channel, modes='-q', params=kwargs.nick)#    解禁
            yield from asyncio.sleep(3*60)
            self.messages[kwargs.host]['black'] -= 1

#!/usr/bin/env python
# encoding: utf-8

import asyncio
from ircaio import IRCProtocol, Events
import logging

def main():
    log = logging.getLogger(__name__)
    event = Events()
    loop = asyncio.get_event_loop()

    coro = loop.create_connection(
        (lambda: IRCProtocol(loop, event, log)),
        **{
            'host':"irc.freenode.net",
            'port':6697,
            'ssl':True
        }
    )

    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    pass

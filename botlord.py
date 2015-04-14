#!/usr/bin/env python
# encoding: utf-8

import asyncio
from ircaio import IRCProtocol
from logging import getLogger, handlers
from json import loads

from botevent import e

def main(config):
    log = getLogger('botlord')
    log.setLevel('DEBUG')

    # Add the log message handler to the logger
    handler = handlers.RotatingFileHandler(filename='botlord.log')

    log.addHandler(handler)


    loop = asyncio.get_event_loop()
    coro = loop.create_connection(
        (lambda: IRCProtocol(config, loop, e, log)),
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
    main(loads(
        open('./xconfig.json', 'r').read()
    ))

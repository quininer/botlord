#!/usr/bin/env python
# encoding: utf-8

import asyncio
from ircaio import IRCProtocol
from logging import getLogger, handlers
from json import loads
from argparse import ArgumentParser

from handle import e

def main(config, logpath=None):
    log = getLogger(config['nick'])
    log.setLevel('DEBUG' if 'debug' in config and config['debug'] else 'INFO')
    handler = handlers.RotatingFileHandler(
        filename=(logpath or '{}.log'.format(config['nick']))
    )
    log.addHandler(handler)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(loop.create_connection(
        (lambda: IRCProtocol(config, loop, e, log)),
        **config['server']
    ))
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', help="config path.")
    parser.add_argument('-l', '--log', help="log path.")
    args = parser.parse_args()

    main(loads(
        open(args.config or './config.json', 'r').read()
    ), args.log)

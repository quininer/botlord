from asyncio import Protocol, Transport
from .pack import pack_command
from .unpack import unpack_command
from functools import partial

from .event import Events
from logging import RootLogger

class IRCProtocol(Protocol):
    def __init__(self, loop, event:Events, log:RootLogger):
        self.loop = loop
        self.event = event
        self.log = log

    def handle(self, event:str, message:str=None):
        event = event.upper()
        self.log.debug(event, message)
        args = {
            event: {'message':message}
        }
        if event == 'DATA' and bool(msg):
            try:
                (command, kwargs) = unpack_command(message)
                self.log.info(command, kwargs)
                args[command] = kwargs
            except ValueError as err:
                self.log.error(err)

        self.__event_handle__(args)

    def __event_handle__(self, args:dict):
        for e in args:
            for i in self.event.__partials__[e]:
                asyncio.async(partial(partial(i, self), **args[e])())
#               asyncio task

    def connection_made(self, transport:Transport):
        self.transport = transport
        self.log.info('Connection made.')
        self.handle('MADE')

    def write(self, data:str):
        data = '{}\r\n'.format(data).encode()
        self.transport.write(data)

    def send(self, command, **kwargs):
        try:
            self.write(pack_command(command, **kwargs))
        except ValueError as err:
            self.log.error(err)

    def data_received(self, data:bytes):
        data = data.decode('utf-8')
        for l in data.split('\r\n'):
            if bool(l.strip()):
                continue
            self.handle('DATA', l)

    def connection_lost(self, exc):
        self.loop.stop()
        self.log.info('Connection lost.')
        self.handle('LOST')

    def eof_received(self):
        self.transport.close()

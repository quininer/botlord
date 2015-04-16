from asyncio import Protocol, async, wait

from pack import pack_command
from unpack import unpack_command
from attrdict import AttrDict
from functools import partial

from os import listdir
from os.path import splitext, isfile, join
from importlib import import_module, reload

class IRCProtocol(Protocol):
    modules = []

    def __init__(self, config:dict, loop, event, log):
        '''
        >>> import logging, asyncio
        >>> from events import Events
        >>> event = Events()
        >>> @event.on('MADE')
        ... def made(bot, kwargs):
        ...     bot.log.info('test.')
        ...     bot.send('QUIT', message="test.")
        >>> log = logging.getLogger('test.log')
        >>> loop = asyncio.get_event_loop()
        >>> coro = loop.create_connection(
        ...     (lambda: IRCProtocol({
        ...         'nick':"testbot",
        ...         'channel':"#testbot"
        ...     }, loop, event, log)),
        ...     **{
        ...         'host':"irc.freenode.net",
        ...         'port':6697,
        ...         'ssl':True
        ...     }
        ... )
        >>> asyncio.iscoroutine(coro)
        True
        >>> type(loop.run_until_complete(coro))
        <class 'tuple'>
        >>> loop.run_forever()
        '''
        self.nick = config['nick']
        self.password = config['password'] if 'password' in config else None
        self.realname = config['realname'] if 'realname' in config else "#linux-cn opbot."
        self.channel = config['channel']
        self.key = config['key'] if 'key' in config else None
        self.master = config['master'] if 'master' in config else None
        self.debug = config['debug'] if 'debug' in config else False

        self.loop = loop
        self.event = event
        self.log = log

    def handle(self, event:str, message:str=None):
        event = event.upper()
        args = {
            event: {'message':message}
        }
        self.log.debug('{}: {!r}'.format(event, message))

        if event == 'DATA' and bool(message):
            try:
                (command, kwargs) = unpack_command(message)
                self.log.debug('{}: {!r}'.format(command, kwargs))
                args[command] = kwargs
            except ValueError as err:
                self.log.warning(err)

        self.__event_handle__(args)

    def __event_handle__(self, args:dict):
        fns = []
        for event in args:
            if not event in self.event.__events__:
                continue
            fns += [partial(e, self)(AttrDict(args[event])) for e in self.event.__events__[event]]

            self.log.debug('{}: {!r}'.format(self.event.__events__[event], args[event]))

#       NOTE asyncio task
        if bool(fns):
            async(wait(fns))

    def connection_made(self, transport):
        '''
        connection made event.
        >>> from asyncio import coroutine
        >>> from events import Events
        >>> event = Events()
        >>> @event.on('MADE')
        ... @coroutine
        ... def made(bot):
        ...     bot.send('NICK', nick=bot.nick)
        >>> made in event.__events__['MADE']
        True
        '''
        self.transport = transport
        self.log.info('Connection made.')
        self.handle('MADE')

    def write(self, data:str):
        '''
        >>> from asyncio import iscoroutine
        >>> from events import Events
        >>> event = Events()
        >>> @event.on('MADE')
        ... def made(bot):
        ...     bot.write("Hello world.")
        >>> iscoroutine(made)
        True
        '''
        self.log.info('[senddata] {}'.format(data))
        data = '{}\r\n'.format(data).encode()
        self.transport.write(data)

    def send(self, command, **kwargs):
        '''
        >>> from asyncio import iscoroutine
        >>> from events import Events
        >>> event = Events()
        >>> @event.on('MADE')
        ... def made(bot):
        ...     bot.send('PRIVMSG', target=nick, message=message)
        >>> iscoroutine(made)
        '''
        try:
            self.write(pack_command(command, **kwargs))
        except ValueError as err:
            self.log.warning(err)

    def data_received(self, data:bytes):
        '''
        data received event.
        >>> from asyncio import iscoroutine
        >>> from events import Events
        >>> event = Events()
        >>> @event.on('DATA')
        ... def data(bot, kwargs):
        ...     bot.log.debug(kwargs.message)
        >>> iscoroutine(data)
        True
        '''
        data = data.decode('utf-8')
        self.log.info('[received] {}'.format(data))
        for l in data.split('\r\n'):
            if bool(l.strip()):
                self.handle('DATA', l)

    def connection_lost(self, exc):
        '''
        connection lost event.
        >>> from asyncio import iscoroutine
        >>> from events import Events
        >>> event = Events()
        >>> @event.on('LOST')
        ... def lost(bot):
        ...     bot.log.info('bye~')
        >>> iscoroutine(lost)
        True
        '''
        self.loop.stop()
        self.log.info('Connection lost.')
        self.handle('LOST')

    def eof_received(self):
        self.transport.close()

    def load_modules(self, re=False):
        self.modules = [
            (reload if re else (lambda x: x))(import_module('modules.{}'.format(module_name))).main(self)
            for module_name in (
                splitext(x)[0] for x in listdir('./modules')
                if (isfile(join('modules', x)) and (not x in ['__init__.py', 'module.py'] and (not x.startswith('.'))))
            )
        ]
        self.log.debug(self.modules)

from asyncio import Protocol, async, wait
from .pack import pack_command
from .unpack import unpack_command
from .attrdict import AttrDict
from functools import partial

class IRCProtocol(Protocol):
    def __init__(self, config:dict, loop, event, log):
        '''
        >>> from events import events
        >>> log = logging.getLogger(__name__)
        >>> loop = asyncio.get_event_loop()
        >>> coro = loop.create_connection(
        ...     (lambda: IRCProtocol({
        ...         'nick':"botlord",
        ...         'channel':"#linux-cn"
        ...     }, loop, event, log)),
        ...     **{
        ...         'host':"irc.freenode.net",
        ...         'port':6697,
        ...         'ssl':True
        ...     }
        ... )
        >>> loop.run_until_complete(coro)
        >>> loop.run_forever()
        '''
        self.nick = config['nick']
        self.password = config['password'] if 'password' in config else None
        self.realname = config['realname'] if 'realname' in config else "#linux-cn opbot."
        self.channel = config['channel']
        self.key = config['key'] if 'key' in config else None
        self.master = config['master'] if 'master' in config else None
        self.operator = config['operator'] if 'operator' in config else []
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
                self.log.info('{}: {!r}'.format(command, kwargs))
                args[command] = kwargs
            except ValueError as err:
                self.log.error(err)

        self.__event_handle__(args)

    def __event_handle__(self, args:dict):
        for event in args:
            if not event in self.event.__events__:
                continue
            fns = [partial(e, self)(AttrDict(args[event])) for e in self.event.__events__[event]]

            self.log.debug('{}: {!r}'.format(self.event.__events__[event], args[event]))

#           NOTE asyncio task
            if bool(fns):
                async(wait(fns))

    def connection_made(self, transport):
        '''
        connection made event.
        >>> @event.on('MADE')
        ... def made(bot)
        ...     bot.send('NICK', nick=bot.nick)
        '''
        self.transport = transport
        self.log.info('Connection made.')
        self.handle('MADE')

    def write(self, data:str):
        '''
        >>> bot.write("Hello world.")
        '''
        self.log.debug('[senddata] {}'.format(data))
        data = '{}\r\n'.format(data).encode()
        self.transport.write(data)

    def send(self, command, **kwargs):
        '''
        >>> bot.send('PRIVMSG', target=nick, message=message)
        '''
        try:
            self.write(pack_command(command, **kwargs))
        except ValueError as err:
            self.log.error(err)

    def data_received(self, data:bytes):
        '''
        data received event.
        >>> @event.on('DATA')
        ... def data(bot, kwargs):
        ...     bot.log.debug(kwargs.message)
        '''
        data = data.decode('utf-8')
        self.log.debug('[received] {}'.format(data))
        for l in data.split('\r\n'):
            if bool(l.strip()):
                self.handle('DATA', l)

    def connection_lost(self, exc):
        '''
        connection lost event.
        >>> @event.on('LOST')
        ... def lost(bot):
        ...     bot.log.info('bye~')
        '''
        self.loop.stop()
        self.log.info('Connection lost.')
        self.handle('LOST')

    def eof_received(self):
        self.transport.close()

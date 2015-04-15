from asyncio import wait
from ircaio import Events

e = Events()

@e.on('MADE')
def MADE(bot, kwargs):
    bot.load_modules()
    yield from wait([module.made() for module in bot.modules])

@e.on('LOST')
def LOST(bot, kwargs):
    yield from wait([module.lost() for module in bot.modules])

@e.on('DATA')
def DATA(bot, kwargs):
    yield from wait([module.data(kwargs) for module in bot.modules])

@e.on('PING')
def PING(bot, kwargs):
    yield from wait([module.ping(kwargs) for module in bot.modules])

@e.on('JOIN')
def JOIN(bot, kwargs):
    yield from wait([module.join(kwargs) for module in bot.modules])

@e.on('PART')
def PART(bot, kwargs):
    yield from wait([module.part(kwargs) for module in bot.modules])

@e.on('PRIVMSG')
def PRIVMSG(bot, kwargs):
    fns = [module.privmsg(kwargs) for module in bot.modules]
    if kwargs.target == bot.nick:
        message = kwargs.message.split(' ', 1)
        message.insert(0, '{}:'.format(bot.nick))
    else:
        message = kwargs.message.split(' ', 2)
    if message[0][:-1] == bot.nick:
        kwargs['command'] = message[1] if len(message) > 1 else None
        kwargs['argument'] = message[2] if len(message) > 2 else None
        fns += [module.command(kwargs) for module in bot.modules]
    yield from wait(fns)

@e.on('NOTICE')
def NOTICE(bot, kwargs):
    yield from wait([module.notice(kwargs) for module in bot.modules])

@e.on('QUIT')
def QUIT(bot, kwargs):
    yield from wait([module.quit(kwargs) for module in bot.modules])

for event in [
    'RPL_WELCOME',
    'RPL_YOURHOST',
    'RPL_CREATED',
    'RPL_MYINFO',
    'RPL_BOUNCE',
    'RPL_MOTDSTART',
    'RPL_MOTD',
    'RPL_ENDOFMOTD',
    'RPL_LUSERCLIENT',
    'RPL_LUSERME',
    'RPL_LUSEROP',
    'RPL_LUSERUNKNOWN',
    'RPL_LUSERCHANNELS',
]:
    e.on(event)(
        (lambda bot, kwargs: (yield from wait([getattr(module, event.lower())(kwargs) for module in bot.modules])))
    )

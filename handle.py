from asyncio import wait
from ircaio import Events

e = Events()

@e.on('MADE')
def MADE(bot, kwargs):
    bot.load_modules()
    yield from wait([m.made() for m in bot.modules])

@e.on('LOST')
def LOST(bot, kwargs):
    pass

@e.on('DATA')
def DATA(bot, kwargs):
    pass

@e.on('PING')
def PING(bot, kwargs):
    yield from wait([m.ping(kwargs) for m in bot.modules])

@e.on('JOIN')
def JOIN(bot, kwargs):
    yield from wait([m.join(kwargs) for m in bot.modules])

@e.on('PART')
def PART(bot, kwargs):
    yield from wait([m.part(kwargs) for m in bot.modules])

@e.on('PRIVMSG')
def PRIVMSG(bot, kwargs):
    em = [m.privmsg(kwargs) for m in bot.modules]
    message = kwargs.message.split(' ', 2)
    if message[0][:-1] == bot.nick:
        kwargs['command'] = message[1] if len(message) > 1 else None
        kwargs['args'] = message[2] if len(message) > 2 else None
        em += [m.command(kwargs) for m in bot.modules]
    yield from wait(em)

@e.on('NOTICE')
def NOTICE(bot, kwargs):
    yield from wait([m.notice(kwargs) for m in bot.modules])

@e.on('QUIT')
def QUIT(bot, kwargs):
    yield from wait([m.quit(kwargs) for m in bot.modules])

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
        (lambda bot, kwargs: (yield from wait([getattr(m, event.lower())(kwargs) for m in bot.modules])))
    )

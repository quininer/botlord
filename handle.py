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
    yield from wait([m.privmsg(kwargs) for m in bot.modules])

@e.on('NOTICE')
def NOTICE(bot, kwargs):
    yield from wait([m.notice(kwargs) for m in bot.modules])

@e.on('QUIT')
def QUIT(bot, kwargs):
    yield from wait([m.quit(kwargs) for m in bot.modules])

@e.on('RPL_WELCOME')
def RPL_WELCOME(bot, kwargs):
    yield from wait([m.rpl_welcome(kwargs) for m in bot.modules])

@e.on('RPL_YOURHOST')
def RPL_YOURHOST(bot, kwargs):
    yield from wait([m.rpl_yourhost(kwargs) for m in bot.modules])

@e.on('RPL_CREATED')
def RPL_CREATED(bot, kwargs):
    yield from wait([m.rpl_created(kwargs) for m in bot.modules])

@e.on('RPL_MYINFO')
def RPL_MYINFO(bot, kwargs):
    yield from wait([m.rpl_myinfo(kwargs) for m in bot.modules])

@e.on('RPL_BOUNCE')
def RPL_BOUNCE(bot, kwargs):
    yield from wait([m.rpl_bounce(kwargs) for m in bot.modules])

@e.on('RPL_MOTDSTART')
def RPL_MOTDSTART(bot, kwargs):
    yield from wait([m.rpl_motdstart(kwargs) for m in bot.modules])

@e.on('RPL_MOTD')
def RPL_MOTD(bot, kwargs):
    yield from wait([m.rpl_motd(kwargs) for m in bot.modules])

@e.on('RPL_ENDOFMOTD')
def RPL_ENDOFMOTD(bot, kwargs):
    yield from wait([m.rpl_endofmotd(kwargs) for m in bot.modules])

@e.on('RPL_LUSERCLIENT')
def RPL_LUSERCLIENT(bot, kwargs):
    yield from wait([m.rpl_luserclitent(kwargs) for m in bot.modules])

@e.on('RPL_LUSERME')
def RPL_LUSERME(bot, kwargs):
    yield from wait([m.rpl_luserme(kwargs) for m in bot.modules])

@e.on('RPL_LUSEROP')
def RPL_LUSEROP(bot, kwargs):
    yield from wait([m.rpl_luserop(kwargs) for m in bot.modules])

@e.on('RPL_LUSERUNKNOWN')
def RPL_LUSERUNKNOWN(bot, kwargs):
    yield from wait([m.rpl_luserunknown(kwargs) for m in bot.modules])

@e.on('RPL_LUSERCHANNELS')
def RPL_LUSERCHANNELS(bot, kwargs):
    yield from wait([m.rpl_luserchannels(kwargs) for m in bot.modules])

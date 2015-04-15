from ircaio import Events

e = Events()

@e.on('MADE')
def MADE(bot, kwargs):
    pass

@e.on('LOST')
def LOST(bot, kwargs):
    pass

@e.on('DATA')
def DATA(bot, kwargs):
    pass

@e.on('PING')
def PING(bot, kwargs):
    pass

@e.on('JOIN')
def JOIN(bot, kwargs):
    pass

@e.on('PART')
def PART(bot, kwargs):
    pass

@e.on('PRIVMSG')
def PRIVMSG(bot, kwargs):
    pass

@e.on('NOTICE')
def NOTICE(bot, kwargs):
    pass

@e.on('QUIT')
def QUIT(bot, kwargs):
    pass

@e.on('RPL_WELCOME')
def RPL_WELCOME(bot, kwargs):
    pass

@e.on('RPL_YOURHOST')
def RPL_YOURHOST(bot, kwargs):
    pass

@e.on('RPL_CREATED')
def RPL_CREATED(bot, kwargs):
    pass

@e.on('RPL_MYINFO')
def RPL_MYINFO(bot, kwargs):
    pass

@e.on('RPL_BOUNCE')
def RPL_BOUNCE(bot, kwargs):
    pass

@e.on('RPL_MOTDSTART')
def RPL_MOTDSTART(bot, kwargs):
    pass

@e.on('RPL_MOTD')
def RPL_MOTD(bot, kwargs):
    pass

@e.on('RPL_ENDOFMOTD')
def RPL_ENDOFMOTD(bot, kwargs):
    pass

@e.on('RPL_LUSERCLIENT')
def RPL_LUSERCLIENT(bot, kwargs):
    pass

@e.on('RPL_LUSERME')
def RPL_LUSERME(bot, kwargs):
    pass

@e.on('RPL_LUSEROP')
def RPL_LUSEROP(bot, kwargs):
    pass

@e.on('RPL_LUSERUNKNOWN')
def RPL_LUSERUNKNOWN(bot, kwargs):
    pass

@e.on('RPL_LUSERCHANNELS')
def RPL_LUSERCHANNELS(bot, kwargs):
    pass

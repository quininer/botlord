from ircaio import Events

e = Events()

@e.on('MADE')
def login(bot, kwargs):
    bot.send('NICK', nick=bot.nick)
    if bool(bot.password):
        bot.log.debug('PASSWORD {}'.format('*'*len(bot.password)))
        bot.send('PASS', password=bot.password)
    if bool(bot.realname):
        bot.send('USER', user=bot.nick, realname=bot.realname)
    bot.send('JOIN', channel=bot.channel)

@e.on('PING')
def keepalive(bot, kwargs):
    bot.log.info(kwargs.message)
    bot.send('PONG', message=kwargs.message)

@e.on('PRIVMSG')
def privmsg(bot, kwargs):
    bot.log.debug('{}'.format(kwargs))
    if kwargs.nick != bot.nick and kwargs.nick != kwargs.target:
       bot.send('PRIVMSG', target=kwargs.target, message='{}: {}'.format(kwargs.nick, kwargs.message))

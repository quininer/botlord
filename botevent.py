from ircaio import Events

e = Events()

@e.on('MADE')
def login(bot, message):
    bot.send('NICK', nick=bot.nick)
    if bool(bot.password):
        bot.log.debug('PASSWORD {}'.format('*'*len(bot.password)))
        bot.send('PASS', password=bot.password)
    if bool(bot.realname):
        bot.send('USER', user=bot.nick, realname=bot.realname)
    bot.send('JOIN', channel=bot.channel)

@e.on('PING')
def keepalive(bot, message):
    bot.log.info(message)
    bot.send('PONG', message=message)

@e.on('PRIVMSG')
def privmsg(bot, user, host, nick, target, message):
    bot.log.debug('{}, {}, {}'.format(nick, target, message))
    if nick != bot.nick and nick != target:
       bot.send('PRIVMSG', target=target, message='{}: {}'.format(nick, message))

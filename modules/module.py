from asyncio import coroutine

class module(object):
    commands = {}

    def __init__(self, bot):
        self.bot = bot
        self.send = bot.send
        self.log = bot.log

    @coroutine
    def made(self):
        pass

    @coroutine
    def lost(self):
        pass

    @coroutine
    def data(self, kwargs):
        pass

    @coroutine
    def privmsg(self, kwargs):
        pass

    @coroutine
    def notice(self, kwargs):
        pass

    @coroutine
    def command(self, kwargs):
        '''
        Trigger:
            /msg #linux-cn botlord: <command>
            /msg botlord <command>

        kwargs = {
            'user': <target user>,
            'host': <target mask>,
            'nick': <target nick>,
            'target': <channel or bot nick>,
            'message': <message>,
            'command': <command name>,
            'argument': <command argument>
        }

        self.commands = {
            '<command name>':<command coroutine function>
        }
        '''
        if not kwargs.command in self.commands:
            return
        self.log.debug(kwargs)
        yield from self.commands[kwargs.command](kwargs)

    @coroutine
    def join(self, kwargs):
        pass

    @coroutine
    def part(self, kwargs):
        pass

    @coroutine
    def quit(self, kwargs):
        pass

    @coroutine
    def rpl_welcome(self, kwargs):
        pass

    @coroutine
    def rpl_yourhost(self, kwargs):
        pass

    @coroutine
    def rpl_created(self, kwargs):
        pass

    @coroutine
    def rpl_myinfo(self, kwargs):
        pass

    @coroutine
    def rpl_bounce(self, kwargs):
        pass

    @coroutine
    def rpl_motdstart(self, kwargs):
        pass

    @coroutine
    def rpl_motd(self, kwargs):
        pass

    @coroutine
    def rpl_endofmotd(self, kwargs):
        pass

    @coroutine
    def rpl_luserclitent(self, kwargs):
        pass

    @coroutine
    def rpl_luserme(self, kwargs):
        pass

    @coroutine
    def rpl_luserop(self, kwargs):
        pass

    @coroutine
    def rpl_luserunknown(self, kwargs):
        pass

    @coroutine
    def rpl_luserchannels(self, kwargs):
        pass

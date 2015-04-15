class module(object):
    def __init__(self, bot):
        self.bot = bot
        self.send = bot.send
        self.log = bot.log

    def made(self):
        pass

    def lost(self):
        pass

    def data(self):
        pass

    def privmsg(self, kwargs):
        pass

    def notice(self, kwargs):
        pass

    def command(self, kwargs):
        '''
        /msg #linux-cn :botlord: <command>
        /msg botlord :<command>
        '''
        pass

    def join(self, kwargs):
        pass

    def part(self, kwargs):
        pass

    def quit(self, kwargs):
        pass

    def rpl_welcome(self, kwargs):
        pass

    def rpl_yourhost(self, kwargs):
        pass

    def rpl_created(self, kwargs):
        pass

    def rpl_myinfo(self, kwargs):
        pass

    def rpl_bounce(self, kwargs):
        pass

    def rpl_motdstart(self, kwargs):
        pass

    def rpl_motd(self, kwargs):
        pass

    def rpl_endofmotd(self, kwargs):
        pass

    def rpl_luserclitent(self, kwargs):
        pass

    def rpl_luserme(self, kwargs):
        pass

    def rpl_luserop(self, kwargs):
        pass

    def rpl_luserunknown(self, kwargs):
        pass

    def rpl_luserchannels(self, kwargs):
        pass

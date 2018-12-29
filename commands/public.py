from . import core


class CommandsPublic(core.Commands):
    def bid(self, text, *a, src, **kw):
        auction = self.client.auction
        if not auction:
            return "There is not currently an auction running."
        elif not text.isdigit():
            return "A bid must be an integer number of USD."
        else:
            bid = int(text)
            bidder = src.nickname
            auction.bid(bid, bidder)

    def authenticate(self, msg, *_):
        return True


# Keep the actual classname unique from this common identifier
# Might make debugging nicer
CommandModule = CommandsPublic

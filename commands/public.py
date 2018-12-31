from . import core


class CommandsPublic(core.Commands):
    async def cmd_bid(self, text, *a, src, **kw):
        auction = self.client.auction
        if not auction:
            return "There is not currently an auction running."
        elif not text.isdigit():
            return "A bid must be an integer number of {}.".format(
                self.client.config.Currency.name_short
            )
        else:
            bid = int(text.strip(self.client.config.Currency.symbol))
            bidder = src.author.name
            ret = auction.bid(bid, bidder)
            if ret:
                await self.client.send("{} has bid {}.".format(bidder, self.client.config.Currency.quantity.format(bid)), src.channel)

    def __authenticate__(self, msg, *_):
        return True


# Keep the actual classname unique from this common identifier
# Might make debugging nicer
CommandModule = CommandsPublic

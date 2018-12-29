from . import auctions, core


class CommandsMod(core.Commands):
    def auction(self, text, *a,
                minimum=5, m=None, time=300, t=None,
                src, **kw):
        try:
            time = int(t or time)
        except:
            return "Time must be an integer number of seconds."
        try:
            minimum = int(m or minimum)
        except:
            return "Minimum must be an integer number of USD."
        auction = self.client.auction
        if text.lower() == "start":
            if auction:
                return "An auction is already running."
            else:
                self.client.send(
                    self.config.Msg.preface.format(
                        auction_length=time,
                        bid_initial=minimum
                    )
                )
                auction = auctions.Auction(self.client, minimum, time)
                self.client.auction = auction
                auction.run()
        elif text.lower() == "stop":
            if not auction:
                return "No auction is currently running."
            else:
                auction.stopped = True
                self.client.auction = None


# Keep the actual classname unique from this common identifier
# Might make debugging nicer
CommandModule = CommandsMod

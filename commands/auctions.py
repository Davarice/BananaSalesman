import datetime as dt
import asyncio


def timeformat(seconds):
    if seconds not in [1]:
        p = "s"
    else:
        p = ""
    if seconds >= 7200:
        return seconds/3600, "hour" + p
    elif seconds >= 120:
        return seconds/60, "minute" + p
    else:
        return seconds, "second" + p


class Bid:
    def __init__(self, bidder, bid):
        self.bidder = bidder
        self.bid = bid
        self.time = dt.datetime.utcnow()

    def __lt__(self, value):
        return self.time < value.time


class Auction:
    def __init__(self, host, minimum, time, channel):
        self.host = host
        self.minimum = minimum
        self.time = time
        self.channel = channel

        self.bids = {}
        self.bidseq = []
        self.ticker = 0
        self.stopped = False
        self.started = None

    def bid(self, bid, bidder):
        if bid < self.minimum:
            return
        lastbid = self.bids.get(bidder, 0)
        if bid > lastbid:
            self.bids[bidder] = bid
            self.bidseq.append(Bid(bidder, bid))
            if self.time - self.ticker < self.host.config.helmet:
                self.time += self.host.config.helmet
            return True

    def top(self):
        if self.bids:
            top_value = max(self.bids.values())
            winners = [x for x in self.bids.keys() if self.bids[x] == top_value]
            if len(winners) > 1:
                latests = []
                for winner in winners:
                    latest = None
                    for bid in self.bidseq:
                        if bid.bidder == winner:
                            latest = bid
                    latests.append(latest)
                winners = [min(latests).bidder]
            return winners, top_value

    async def run(self):
        self.ticker = 0
        self.started = dt.datetime.utcnow()

        await self.host.send(self.host.config.Msg.start, self.channel)
        while self.ticker < self.time and not self.stopped:
            await asyncio.sleep(1)
            self.ticker += 1
            left = self.time - self.ticker
            if left in self.host.config.important_seconds:
                await self.host.send(self.host.config.Msg.timer.format(left, "seconds"), self.channel)

        if self.stopped:
            await self.stop()
        else:
            await self.end()

    async def finish(self):
        self.host.auction = None
        results = self.top()
        if not results:
            phrase = self.host.config.Msg.results_none
            results = [None], None
        elif len(results[0]) == 1:
            phrase = self.host.config.Msg.results_one
        else:
            phrase = self.host.config.Msg.results_tie
        await self.host.send(phrase.format(winners=results[0],price=results[1]), self.channel)

    async def end(self):
        await self.host.send(self.host.config.Msg.end, self.channel)
        await self.finish()

    async def stop(self):
        await self.host.send(self.host.config.Msg.stop, self.channel)
        await self.finish()

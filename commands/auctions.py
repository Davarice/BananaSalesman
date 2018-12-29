import datetime as dt


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


class Auction:
    def __init__(self, host, minimum, time):
        self.host = host
        self.minimum = minimum
        self.time = time

        self.bids = {}
        self.ticker = 0
        self.stopped = False
        self.started = None

    def bid(self, bid, bidder):
        if bid < self.minimum:
            return
        lastbid = self.bids.get(bidder, 0)
        if bid > lastbid:
            self.bids[bidder] = bid

    def run(self):
        self.host.send(self.host.config.Msg.start)
        self.started = dt.datetime.utcnow()

    def check(self):
        if self.stopped:
            self.stop()
        elif dt.datetime.utcnow() > self.started + dt.timedelta(seconds=self.time):
            self.end()

    def top(self):
        if self.bids:
            top_value = max(self.bids.values())
            winners = [x for x in self.bids.keys() if self.bids[x] == top_value]
            return winners, top_value

    def finish(self):
        self.host.auction = None
        results = self.top()
        if not results:
            phrase = self.host.config.Msg.results_none
            results = [None], None
        elif len(results[0]) == 1:
            phrase = self.host.config.Msg.results_one
        else:
            phrase = self.host.config.Msg.results_tie
        self.host.send(phrase.format(winners=results[0],price=results[1]))

    def end(self):
        self.host.send(self.host.config.Msg.end)
        self.finish()

    def stop(self):
        self.host.send(self.host.config.Msg.stop)
        self.finish()

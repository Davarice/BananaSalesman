import sys
import time

from twitchobserver import Observer

import commands
import config


username = sys.argv[1]
oauth = sys.argv[2]
channel = sys.argv[3]


class Bot:
    def __init__(self, name, token):
        self.client = Observer(name, token)
        self.config = config
        self.commands = commands.CommandRouter(self)

        self.auction = None
        self.lastout = ""

    def process_event(self, event):
        if event.type == "TWITCHCHATMESSAGE":
            retval = self.commands.run(src=event)
            if retval and type(retval) == str:
                retval = retval.format(
                    channel=event.channel,
                    author=event.tags["display-name"],
                    original=event.message,
                )
                self.client.send_message(retval, event.channel)

    def process_all(self):
        for event in self.client.get_events():
            self.process_event(event)

    def send(self, text, dest=None):
        out = str(text).strip()
        if out and out != self.lastout:
            self.lastout = out
            self.client.send_message(out, dest or channel)


def run():
    global bot
    bot = Bot(username, oauth)
    bot.client.start()
    bot.client.join_channel(channel)
    print("Channel {} joined".format(channel))

    while True:
        try:
            time.sleep(bot.config.refresh)

            bot.process_all()
            if bot.auction:
                bot.auction.check()

        except KeyboardInterrupt:
            print("Closing down...")
            break

    bot.client.leave_channel(channel)
    bot.client.stop()


if __name__ == "__main__":
    run()

import time
import sys

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

    def process_event(self, event):
        # print(event)
        if event.type == "TWITCHCHATMESSAGE":
            retval = self.commands.run(src=event)
            if retval:
                self.client.send_message(retval, event.channel)

    def process_all(self):
        for event in self.client.get_events():
            self.process_event(event)

    def send(self, text, dest=None):
        self.client.send_message(text, dest or channel)


def run():
    bot = Bot(username, oauth)
    bot.client.start()
    bot.client.join_channel(channel)
    print("Channel {} joined".format(channel))

    while True:
        try:
            bot.process_all()
            time.sleep(bot.config.refresh)
        except KeyboardInterrupt:
            print("Closing down...")
            break

    bot.client.leave_channel(channel)
    bot.client.stop()


if __name__ == "__main__":
    run()

import sys

from twitchio.ext import commands as twitch

import commands
import config


username = sys.argv[1]
client_key = sys.argv[2]
oauth = sys.argv[3]
channel = sys.argv[4]


# api token can be passed as test if not needed.
# Channels is the initial channels to join, this could be a list, tuple or callable
interface = twitch.Bot(
    irc_token=oauth,
    client_id=client_key,
    nick=username,
    prefix=config.prefix,
    initial_channels=[channel]
)


class Bot:
    def __init__(self):
        self.client = interface
        self.config = config
        self.commands = commands.CommandRouter(self)

        self.auction = None
        self.lastout = ""

    async def send(self, text, dest):
        out = str(text).strip()
        if out and out != self.lastout:
            self.lastout = out
            print(out)
            await dest.send(out)


bot = Bot()


# Register an event with the interface
@interface.event
async def event_ready():
    print(f'Ready | {interface.nick}')


@interface.event
async def event_message(message):
    print(str(message.author) + " -> " + message.content)

    retval = await bot.commands.run(src=message)
    if retval and type(retval) == str:
        retval = retval.format(
            channel=message.channel.name,
            author=message.tags["display-name"],
            original=message.content,
        )
        await bot.send(retval, message.channel)


# Register a command with the bot
@interface.command(name='test', aliases=['t'])
async def test_command(ctx):
    await ctx.send(f'Hello {ctx.author.name}')


if __name__ == "__main__":
    bot.client.run()

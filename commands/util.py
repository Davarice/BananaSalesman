from . import core


class CommandsUtil(core.Commands):
    async def cmd_echo(self, text, *a, loud=False, src, **kw):
        if loud is True:
            return "{} said '{}'".format(src.author.name, text.upper())
        else:
            return "{} said '{}'".format(src.author.name, text)


# Keep the actual classname unique from this common identifier
# Might make debugging nicer
CommandModule = CommandsUtil

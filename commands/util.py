from . import core


class CommandsUtil(core.Commands):
    def echo(self, text, *a, src, **kw):
        return "{} said '{}'".format(src.nickname, text)

    def echo2(self, text, *a, loud=False, src, **kw):
        if loud is True:
            return "{} said '{}'".format(src.nickname, text.upper())
        else:
            return "{} said '{}'".format(src.nickname, text)


# Keep the actual classname unique from this common identifier
# Might make debugging nicer
CommandModule = CommandsUtil

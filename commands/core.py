class Commands:
    def __init__(self, client, router, *a, **kw):
        self.client = client
        self.config = client.config
        self.router = router
        self.args = a  # Save for later
        self.kwargs = kw  # Just in case

    def __get_command__(self, kword):
        if "__" not in kword:
            # Deny existence of any __methods__
            return getattr(self, kword, None)

    def __authenticate__(self, msg, *_):
        """
        Take a Discord message and return True if:
          1. The author of the message is allowed to access this package
          2. This command can be run in this channel
        Should be overwritten by modules providing secure functions
        (For example, moderation tools)
        """
        if (
            "moderator/1" in msg.tags["badges"]
            or "broadcaster/1" in msg.tags["badges"]
            or msg.author.name in self.config.devs
        ):
            return True

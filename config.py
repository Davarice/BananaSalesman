devs = ["davarice"]

prefix = "+"
refresh = 0.1


class Currency:
    # Information about money that the bot needs to know
    name_short = "USD"
    name_full_single = "US Dollar"
    name_full_plural = "US Dollars"

    symbol = "$"
    quantity = symbol + "{}"


class Msg:
    preface = (
        "The Auction will run for {auction_length} seconds."
        + " Enter a bid by posting '{}bid <amount>'.".format(prefix)
        + " Focus on chat and not any 'live' video of the chat since there might be a slight delay."
        # + " I will confirm bids in chat."
        # + " I will do a final 5,4,3,2,1,0 countdown after which the auction is over."
        + " The person with the highest bid will be declared the winner and they will have to tip that amount to claim their prize. Bidding starts at {}.".format(
            Currency.quantity.format("{bid_initial}")
        )
    )

    results_none = "Nobody has offered to pay the minimum bid or more...*sniff*"
    results_one = (
        "{winners[0]} is the highest bidder, with an offer of "
        + "{}!".format(Currency.quantity.format("{price}"))
    )
    results_tie = (
        "The Auction is a TIE! The following people have all offered "
        + Currency.quantity.format("{price}")
        + ": {winners}"
    )

    start = "The Auction begins NOW."
    end = "The Auction has ended."
    stop = "The Auction has been stopped."

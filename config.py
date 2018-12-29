devs = ["davarice"]

prefix = "+"
refresh = 0.1

class Msg:
    preface = "blah blah starting"
    preface2 = (
        "The Auction will run for {auction_length} seconds. Focus on chat and not any 'live' video since there might be a slight delay."
        # + " I will confirm bids in chat."
        # + " I will do a final 5,4,3,2,1,0 countdown after which the auction is over."
        + " The person with the highest bid will be declared the winner and they will have to tip that amount to claim their prize. Bidding starts at ${bid_initial}."
    )

    results_none = "Nobody has offered to pay the minimum bid or more...*sniff*"
    results_one = "{winners[0]} is the highest bidder, with an offer of ${price}!"
    results_tie = "The Auction is a TIE! The following people have all offered ${price}: {winners}"

    start = "The Auction begins NOW."
    end = "The Auction has ended."
    stop = "The Auction has been stopped."

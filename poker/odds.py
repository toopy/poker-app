from poker import table


# http://en.wikipedia.org/wiki/Poker_probability
# http://en.wikipedia.org/wiki/Poker_probability_(Texas_hold_%27em)


PREFLOP = [
    331,
    220,
    81.9,
    81.9,
    72.7,
    54.3,
    54.3,
    43.2,
    32.2,
    24.5,
    19.7,
    19.1,
    10.1,
    5.98,
    5.38,
    3.81,
    .873,
]


class Odds(object):

    def __init__(self, cards, hand, turn):
        self.cards = cards
        self.hand = hand
        self.turn = turn

    def get_preflop_odds(self):
        return PREFLOP[self.hand]

    def get_flop_odds(self):
        return None

    def get_turn_odds(self):
        return None

    def get_river_odds(self):
        return None

    def get_odds(self):
        if self.turn == table.PREFLOP:
            return self.get_preflop_odds()
        if self.turn == table.FLOP:
            return self.get_flop_odds()
        if self.turn == table.TURN:
            return self.get_turn_odds()
        if self.turn == table.RIVER:
            return self.get_river_odds()

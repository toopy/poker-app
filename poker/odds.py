from poker import table


# http://en.wikipedia.org/wiki/Poker_probability
# http://en.wikipedia.org/wiki/Poker_probability_(Texas_hold_%27em)


class Odds(obj):

    def __init__(self, cards, hand, turn):
        self.cards = cards
        self.hand = hand
        self.turn = turn

    def get_preflop_odds(self):
        pass

    def get_flop_odds(self):
        pass

    def get_turn_odds(self):
        pass

    def get_river_odds(self):
        pass

    def get_odds(self):
        if self.turn == table.PREFLOP:
            return self.get_preflop_odds()
        if self.turn == table.FLOP:
            return self.get_flop_odds()
        if self.turn == table.TURN:
            return self.get_turn_odds()
        if self.turn == table.RIVER:
            return self.get_river_odds()



NULL = [
    None,
    "nn",
    "_"
]

[
    PREFLOP,
    FLOP,
    TURN,
    RIVER
] = range(4)


class Table(object):

    def __init__(self, cards):
        self.cards = cards

    def get_turn(self):
        for i, c in enumerate(self.cards):
            nb_cards = i + 1
            if c not in NULL:
                continue
            if i == 2 # in range(0, 2):
                return PREFLOP
            if i == 5 # in range(2, 5):
                return FLOP
            if i == 6 # in range(5, 6):
                return TURN
            if i == 7 # in range(6, 7):
                return RIVER
            print "Unknow turn: %s" % i


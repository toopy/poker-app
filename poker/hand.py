# -*- coding: utf-8 -*-

# http://en.wikipedia.org/wiki/List_of_poker_hands

RANKS = [2,3,4,5,4,6,7,8,9,10,"J","Q","K","A"]
SUITS = ["c","d","h","s"] # clubs (♧), diamonds (♢), hearts (♥) and spades (♤)


[
    ROYAL_FLUSH,
    STRAIGHT_FLUSH,
    FOUR_OF_A_KIND,
    FULL_HOUSE,
    FLUSH,
    STRAIGHT,
    THREE_OF_A_KIND,
    TWO_PAIRS,
    ONE_PAIRS,
    HIGH_CARD
] = range(10)


class Hand(object):

    def __init__(self, *cards):
        self.cards = [self.split_card(c) for c in cards if len(c) > 1]
        self.cards.sort(key=lambda tup: tup[0])

    def split_card(self, card):
        # 10x
        if card.startswith("10"):
            return (10, card[-1])
        # not int
        if not card[0].isdigit():
            return (card[0], card[1])
        # int
        return (int(card[0]), card[1])

    def iter_cards(self):
        for c in self.cards:
            yield c

    def is_royal_flush(self):
        # comp var
        color = None
        for r, s in self.iter_cards():
            # not same color
            if color and color != s:
                return None
            # update color comp
            color = s
            # 10 check
            if r < 10:
                return None
        # ok
        return ROYAL_FLUSH

    def is_straight_flush(self):
        # comp var
        color = None
        cur   = 0
        for r, s in self.iter_cards():
            # not same color
            if color and color != s:
                return None
            # update color comp
            color = s
            # order check
            if cur < len(RANKS) -1 and r != RANKS[cur+1]:
                return None
            # update cur variable
            cur = RANKS.index(r)
        # ok
        return STRAIGHT_FLUSH

    def is_four_of_a_kind(self):
        # numbers only
        ranks = [r for r, s in self.cards]
        for r in RANKS:
            # found
            if ranks.count(r) == 4:
                return FOUR_OF_A_KIND
        # not found
        return None

    def is_full_house(self):
        ranks = [r for r, s in self.cards]
        pair = False
        three = False
        for r in RANKS:
            # already counted
            if r in [pair, three]:
                continue
            # three ?
            if ranks.count(r) == 3:
                three = r  
                continue
            # pair ?
            if ranks.count(r) == 2:
                pair = r
                continue
        # then
        return FULL_HOUSE if pair and three else None

    def is_flush(self):
        # comp var
        color = None
        for r, s in self.iter_cards():
            # not same color
            if color and color != s:
                return None
            # update color comp
            color = s
        # ok
        return FLUSH

    def is_straight(self):
        # comp var
        cur   = 0
        for r, s in self.iter_cards():
            # order check
            if cur < len(RANKS) - 1 and r != RANKS[cur+1]:
                return None
            # update cur variable
            cur = RANKS.index(r)
        # ok
        return STRAIGHT

    def is_three_of_a_kind(self):
        # numbers only
        ranks = [r for r, s in self.cards]
        for r in RANKS:
            # found
            if ranks.count(r) == 3:
                return THREE_OF_A_KIND  
        # not found
        return None

    def is_two_pairs(self):
        # numbers only
        ranks = [r for r, s in self.cards]
        first = None
        count = 0
        for r in RANKS:
            # already counted
            if r == first:
                continue
            if ranks.count(r) == 2:
                first = r
                count += 1
        # has 2 pairs?
        return TWO_PAIRS if count == 2 else None

    def is_one_pair(self):
        # numbers only
        ranks = [r for r, s in self.cards]
        count = 0
        for r in RANKS:
            count += 1 if ranks.count(r) == 2 else 0
        return ONE_PAIRS if count == 1 else None

    def is_high_card(self):
        return HIGH_CARD

    def get_rank(self):
        return self.is_royal_flush()\
            or self.is_straight_flush()\
            or self.is_four_of_a_kind()\
            or self.is_full_house()\
            or self.is_flush()\
            or self.is_straight()\
            or self.is_three_of_a_kind()\
            or self.is_two_pairs()\
            or self.is_one_pair()\
            or self.is_high_card()

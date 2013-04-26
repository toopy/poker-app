# -*- coding: utf-8 -*-

# http://en.wikipedia.org/wiki/List_of_poker_hands

RANKS = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]

[
    TWO,
    THREE,
    FOUR,
    FIVE,
    SIX,
    SEVEN,
    EIGHT,
    NINE,
    TEN,
    JAKE,
    QUEEN,
    KING,
    AS,
] = range(13)

SUITS = ["c","d","h","s"] # clubs (♧), diamonds (♢), hearts (♥) and spades (♤)


class HandBase(object):

    def __init__(self, *cards):
        self.cards = [self.split_card(c) for c in cards if len(c) > 1]
        self.cards.sort(key=lambda tup: tup[0])

    def split_card(self, card):
        # little check
        if not len(card) in [2, 3]:
            print 'h:bad len:%s' % len(card)
            return (None, None)
        # parse suit
        s = card[-1].lower()
        # little check
        if not s in SUITS:
            print 'h:bad suit:%s' % s
            return (None, None)
        # parse rank
        r = card[0].upper()
        # little check
        if not r in RANKS:
            print 'h:bad rank:%s' % r
            return None, None
        # OK
        return (RANKS.index(r), s)

    def iter_cards(self):
        for c in self.cards:
            yield c


[
    ZERO,
    _9__2,
    _9_MORE,
    T9__32,
    T_MORE,
    J_MORE,
    Q_MORE,
    AQS__QTS,
    T9S__32S,
    JT,
    TT,
    KQ_QJ,
    JJ,
    KK_QQ,
    AK,
    KQS_QJS_JTS,
    AA,
    AKS,
] = range(18)


PREFLOP_NAMES = [
    '',
    '9 > 2',
    '9 more',
    'T9 > 32',
    'T more',
    'J more',
    'Q more',
    'AQS > QTS',
    'T9S > 32S',
    'JT',
    'TT',
    'KQ QJ',
    'JJ',
    'KK QQ',
    'AK',
    'KQS QJS JTS',
    'AA',
    'AKS',
]


class HandPreflop(HandBase):

    def is_aks(self):
        """AKs (or any specific suited cards)
        """
        color = None
        for r, s in self.iter_cards():
            if r not in [KING, AS]:
                return None 
            if color and color != s:
                return None
            color = s 
        return AKS

    def is_aa(self):
        """AA (or any specific pair)
        """
        for r, s in self.iter_cards():
            if r not in [AS]:
                return None 
        return AA

    def is_kqs_qjs_jts(self):
        """AKs, KQs, QJs, or JTs (suited cards)
        """
        rank = None
        suit = None
        for r, s in self.iter_cards():
            if rank is not None\
            and r != rank + 1:
                return None
            if suit is not None\
            and s != suit:
                return None
            if r < TEN:
                return None
            rank = r
            suit = s
        return KQS_QJS_JTS

    def is_ak(self):
        """AK (or any specific non-pair incl. suited)
        """
        rank = None
        for r, s in self.iter_cards():
            if r not in [KING, AS]:
                return None 
            if rank and r != rank + 1:
                return None
            rank = r
        return AK

    def is_kk_qq(self):
        """AA, KK, or QQ
        """
        rank = None
        for r, s in self.iter_cards():
            if r not in [QUEEN, KING]:
                return None 
            if not rank:
                rank = r
            if rank != r:
                return None
        return KK_QQ

    def is_jj(self):
        """AA, KK, QQ or JJ
        """
        for r, s in self.iter_cards():
            if r not in [JAKE]:
                return None 
        return JJ

    def is_kq_qj(self):
        """Suited cards, jack or better
        """
        rank = None
        for r, s in self.iter_cards():
            if rank is not None\
            and r != rank + 1:
                return None
            if r < JAKE:
                return None
            rank = r
        return KQ_QJ

    def is_tt(self):
        """AA, KK, QQ, JJ, or TT
        """
        for r, s in self.iter_cards():
            if r not in [TEN]:
                return None 
        return TT

    def is_jt(self):
        """Suited cards, 10 or better
        """
        rank = None
        for r, s in self.iter_cards():
            if rank is not None\
            and r != rank + 1:
                return None
            if r < TEN:
                return None
            rank = r
        return JT

    def is_t9s__32s(self):
        """Suited connectors
        """
        rank = None
        suit = None
        for r, s in self.iter_cards():
            if rank is not None\
            and r != rank + 1:
                return None
            if suit is not None\
            and s != suit:
                return None
            rank = r
            suit = s
        return T9S__32S

    def is_aqs__qts(self):
        """Connected cards, 10 or better
        """
        rank = None
        suit = None
        for r, s in self.iter_cards():
            if r < TEN:
                return None
            if suit is not None\
            and s != suit:
                return None
            rank = r
            suit = s
        return AQS__QTS

    def is_q_more(self):
        """Any 2 cards with rank at least queen
        """
        for r, s in self.iter_cards():
            if r < QUEEN:
                return None 
        return Q_MORE

    def is_j_more(self):
        """Any 2 cards with rank at least jack
        """
        for r, s in self.iter_cards():
            if r < JAKE:
                return None 
        return J_MORE

    def is_t_more(self):
        """Any 2 cards with rank at least 10
        """
        for r, s in self.iter_cards():
            if r < TEN:
                return None 
        return T_MORE

    def is_t9__32(self):
        """Connected cards (cards of consecutive rank)
        """
        rank = None
        for r, s in self.iter_cards():
            if rank is not None\
            and r != rank + 1:
                return None
            rank = r
        return T9__32

    def is_9_more(self):
        """Any 2 cards with rank at least 9
        """
        for r, s in self.iter_cards():
            if r < NINE:
                return None 
        return _9_MORE

    def is_9__2(self):
        """Not connected nor suited, at least one 2-9
        """
        return _9__2

    def get_rank(self):
        return self.is_aks()\
         or self.is_aa()\
         or self.is_kqs_qjs_jts()\
         or self.is_ak()\
         or self.is_kk_qq()\
         or self.is_jj()\
         or self.is_kq_qj()\
         or self.is_tt()\
         or self.is_jt()\
         or self.is_t9s__32s()\
         or self.is_aqs__qts()\
         or self.is_q_more()\
         or self.is_j_more()\
         or self.is_t_more()\
         or self.is_t9__32()\
         or self.is_9_more()\
         or self.is_9__2()

    @staticmethod
    def get_name(rank):
        return '' if not rank else PREFLOP_NAMES[rank]


[
    ZERO,
    HIGH_CARD,
    ONE_PAIR,
    TWO_PAIRS,
    THREE_OF_A_KIND,
    STRAIGHT,
    FLUSH,
    FULL_HOUSE,
    FOUR_OF_A_KIND,
    STRAIGHT_FLUSH,
    ROYAL_FLUSH,
] = range(11)

NAMES = [
    'zero',
    'high card',
    'one pair',
    'two pairs',
    'three of a kind',
    'straight',
    'flush',
    'full house',
    'four of a kind',
    'straight flush',
    'royal flush',
]


class Hand(HandBase):

    def is_royal_flush(self):
        # comp var
        suit = None
        for r, s in self.iter_cards():
            # not same suit
            if suit and suit != s:
                return None
            # update suit comp
            suit = s
            # 10 check
            if r < TEN:
                return None
        # ok
        return ROYAL_FLUSH

    def is_straight_flush(self):
        # comp var
        suit = None
        rank = 0
        for r, s in self.iter_cards():
            # not same suit
            if suit and suit != s:
                return None
            # update suit comp
            suit = s
            # order check
            if rank and r != rank + 1:
                return None
            # update rank variable
            rank = r
        # ok
        return STRAIGHT_FLUSH

    def is_four_of_a_kind(self):
        # numbers only
        ranks = [r for r, s in self.cards]
        for r in ranks:
            # found
            if ranks.count(r) == 4:
                return FOUR_OF_A_KIND
        # not found
        return None

    def is_full_house(self):
        ranks = [r for r, s in self.cards]
        pair = False
        three = False
        for r in ranks:
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
        suit = None
        for r, s in self.iter_cards():
            # not same suit
            if suit and suit != s:
                return None
            # update suit comp
            suit = s
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
        for r in ranks:
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
        for r in ranks:
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
        first = None
        for r in ranks:
            # already counted
            if r == first:
                continue
            if ranks.count(r) == 2:
                first = r
                count += 1
        return ONE_PAIR if count == 1 else None

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

    @staticmethod
    def get_name(rank):
        return '' if not rank else NAMES[rank]

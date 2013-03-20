import unittest

from poker import hand


class TestHandPreflop(unittest.TestCase):

    def test_is_aks(self):
        cards = ['As', 'Ks']
        h = hand.HandPreflop(*cards)
        self.assertEqual(h.is_aks(), hand.AKS)
        self.assertEqual(h.get_rank(), hand.AKS)

    def test_is_aa(self):
        cards = ['As', 'Ac']
        h = hand.HandPreflop(*cards)
        self.assertEqual(h.is_aa(), hand.AA)
        self.assertEqual(h.get_rank(), hand.AA)

    def test_is_kqs_qjs_jts(self):
        cards_to_test = [
            ['Ks', 'Qs'],
            ['Qs', 'Js'],
            ['Js', 'Ts'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_kqs_qjs_jts(), hand.KQS_QJS_JTS)
            self.assertEqual(h.get_rank(), hand.KQS_QJS_JTS)

    def test_is_ak(self):
        cards_to_test = [
            ['Ks', 'Ad'],
            ['As', 'Kc'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_ak(), hand.AK)
            self.assertEqual(h.get_rank(), hand.AK)

    def test_is_kk_qq(self):
        cards_to_test = [
            ['Ks', 'Kd'],
            ['Qs', 'Qc'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_kk_qq(), hand.KK_QQ)
            self.assertEqual(h.get_rank(), hand.KK_QQ)

    def test_is_jj(self):
        cards_to_test = [
            ['Js', 'Jd'],
            ['Js', 'Jc'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_jj(), hand.JJ)
            self.assertEqual(h.get_rank(), hand.JJ)

    def test_is_kq_qj(self):
        cards_to_test = [
            ['Ks', 'Qd'],
            ['Qs', 'Jc'],
            ['Jd', 'Qc'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_kq_qj(), hand.KQ_QJ)
            self.assertEqual(h.get_rank(), hand.KQ_QJ)

    def test_is_tt(self):
        cards_to_test = [
            ['Ts', 'Td'],
            ['Ts', 'Tc'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_tt(), hand.TT)
            self.assertEqual(h.get_rank(), hand.TT)

    def test_is_jt(self):
        cards_to_test = [
            ['Js', 'Td'],
            ['Ts', 'Jc'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_jt(), hand.JT)
            self.assertEqual(h.get_rank(), hand.JT)

    def test_is_t9s__32s(self):
        cards_to_test = [
            ['Ts', '9s'],
            ['7c', '8c'],
            ['4d', '5d'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_t9s__32s(), hand.T9S__32S)
            self.assertEqual(h.get_rank(), hand.T9S__32S)

    def test_is_q_more(self):
        cards_to_test = [
            ['Ac', 'Qs'],
            ['Qd', 'Ac'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_q_more(), hand.Q_MORE)
            self.assertEqual(h.get_rank(), hand.Q_MORE)

    def test_is_j_more(self):
        cards_to_test = [
            ['Ac', 'Js'],
            ['Jd', 'Kc'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_j_more(), hand.J_MORE)
            self.assertEqual(h.get_rank(), hand.J_MORE)

    def test_is_t_more(self):
        cards_to_test = [
            ['Ac', 'Ts'],
            ['Td', 'Kc'],
            ['Qs', 'Th'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_t_more(), hand.T_MORE)
            self.assertEqual(h.get_rank(), hand.T_MORE)

    def test_is_t9__32(self):
        cards_to_test = [
            ['9c', '8s'],
            ['5d', '6c'],
            ['3s', '2h'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_t9__32(), hand.T9__32)
            self.assertEqual(h.get_rank(), hand.T9__32)

    def test_is_9_more(self):
        cards_to_test = [
            ['Jc', '9s'],
            ['9d', 'Kc'],
            ['Qs', '9h'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_9_more(), hand._9_MORE)
            self.assertEqual(h.get_rank(), hand._9_MORE)

    def test_is_9__2(self):
        cards_to_test = [
            ['2c', '9s'],
            ['4d', '8c'],
            ['5s', '3h'],
        ]
        for cards in cards_to_test: 
            h = hand.HandPreflop(*cards)
            self.assertEqual(h.is_9__2(), hand._9__2)
            self.assertEqual(h.get_rank(), hand._9__2)

class TestHand(unittest.TestCase):

    def test_is_royal_flush(self):
        cards_to_test = [
            ['Tc', 'Jc', 'Qc', 'Kc', 'Ac'],
            ['Js', 'Ks', 'Qs', 'As', 'Ts'],
            ['Td', 'Ad', 'Kd', 'Jd', 'Qd'],
        ]
        for cards in cards_to_test: 
            h = hand.Hand(*cards)
            self.assertEqual(h.is_royal_flush(), hand.ROYAL_FLUSH)
            self.assertEqual(h.get_rank(), hand.ROYAL_FLUSH)

    def test_is_straight_flush(self):
        cards_to_test = [
            ['9c', 'Tc', 'Jc', 'Qc', 'Kc'],
            ['Js', 'Qs', 'Ts', '8s', '9s'],
            ['Td', '6d', '9d', '7d', '8d'],
        ]
        for cards in cards_to_test: 
            h = hand.Hand(*cards)
            self.assertEqual(h.is_straight_flush(), hand.STRAIGHT_FLUSH)
            self.assertEqual(h.get_rank(), hand.STRAIGHT_FLUSH)

    def test_is_four_of_a_kind(self):
        cards_to_test = [
            ['9c', 'Tc', '9s', '9d', '9h'],
            ['Qd', 'Qc', 'Qh', '8s', 'Qs'],
            ['Td', 'Ad', 'As', 'Ac', 'Ah'],
        ]
        for cards in cards_to_test: 
            h = hand.Hand(*cards)
            self.assertEqual(h.is_four_of_a_kind(), hand.FOUR_OF_A_KIND)
            self.assertEqual(h.get_rank(), hand.FOUR_OF_A_KIND)

    def test_is_full_house(self):
        cards_to_test = [
            ['9c', 'Tc', '9s', 'Td', 'Th'],
            ['Ad', 'Ac', 'Qh', 'As', 'Qs'],
            ['5d', 'Ad', 'As', '5c', '5h'],
        ]
        for cards in cards_to_test: 
            h = hand.Hand(*cards)
            self.assertEqual(h.is_full_house(), hand.FULL_HOUSE)
            self.assertEqual(h.get_rank(), hand.FULL_HOUSE)

    def test_is_flush(self):
        cards_to_test = [
            ['9c', 'Tc', '5c', 'Jc', 'Kc'],
            ['Ad', '2d', '6d', 'Td', 'Qd'],
            ['Jh', 'Kh', '3h', '6h', '5h'],
        ]
        for cards in cards_to_test: 
            h = hand.Hand(*cards)
            self.assertEqual(h.is_flush(), hand.FLUSH)
            self.assertEqual(h.get_rank(), hand.FLUSH)

    def test_is_straight(self):
        cards_to_test = [
            ['9c', 'Tc', '5c', 'Jc', 'Kc'],
            ['Ad', '2d', '6d', 'Td', 'Qd'],
            ['Jh', 'Kh', '3h', '6h', '5h'],
        ]
        for cards in cards_to_test: 
            h = hand.Hand(*cards)
            self.assertEqual(h.is_flush(), hand.FLUSH)
            self.assertEqual(h.get_rank(), hand.FLUSH)

    def test_is_three_of_a_kind(self):
        cards_to_test = [
            ['9c', 'Tc', '5c', 'Ts', 'Td'],
            ['Ad', 'Qs', 'Qh', 'Td', 'Qd'],
            ['3c', '3s', '3h', '6h', '5h'],
        ]
        for cards in cards_to_test: 
            h = hand.Hand(*cards)
            self.assertEqual(h.is_three_of_a_kind(), hand.THREE_OF_A_KIND)
            self.assertEqual(h.get_rank(), hand.THREE_OF_A_KIND)

    def test_is_two_pairs(self):
        cards_to_test = [
            ['9c', 'Ac', '9s', 'Ts', 'Td'],
            ['3d', 'Qs', 'Qh', 'Td', '3c'],
            ['3c', '5s', '3h', '6h', '5h'],
        ]
        for cards in cards_to_test: 
            h = hand.Hand(*cards)
            self.assertEqual(h.is_two_pairs(), hand.TWO_PAIRS)
            self.assertEqual(h.get_rank(), hand.TWO_PAIRS)

    def test_is_one_pair(self):
        cards_to_test = [
            ['9c', 'Ac', '9s', 'Ts', 'Qd'],
            ['3d', 'Qs', '8h', 'Td', '3c'],
            ['3c', '5s', 'Ah', '6h', '5h'],
        ]
        for cards in cards_to_test: 
            h = hand.Hand(*cards)
            self.assertEqual(h.is_one_pair(), hand.ONE_PAIR)
            self.assertEqual(h.get_rank(), hand.ONE_PAIR)

    def test_is_high_card(self):
        cards_to_test = [
            ['9c', 'Ac', '2s', 'Ts', 'Qd'],
            ['4d', 'Qs', '8h', 'Td', '3c'],
            ['3c', '5s', 'Ah', '6h', 'Jh'],
        ]
        for cards in cards_to_test: 
            h = hand.Hand(*cards)
            self.assertEqual(h.is_high_card(), hand.HIGH_CARD)
            self.assertEqual(h.get_rank(), hand.HIGH_CARD)

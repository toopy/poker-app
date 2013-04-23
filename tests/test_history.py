import unittest

from poker import history


class TestHistoryLine(unittest.TestCase):

    def test_no_no_turn(self):
        h = history.History()
        l = "Siege 1: genie001 s'est couche. sur le Tournant"
        self.assertEquals(h.parse_line(l), {
            'player': 'genie001',
            'info': history.INFO_NONE,
            'win': history.WIN_LOOSE,
            'when': history.WHEN_TURN,
        })

    def test_button_no_preflopwithout(self):
        h = history.History()
        l = "Siege 4: TFC37 (bouton) s'est couche. avant Flop (n'a pas mise)"
        self.assertEquals(h.parse_line(l), {
            'player': 'TFC37',
            'info': history.INFO_BUTTON,
            'win': history.WIN_LOOSE,
            'when': history.WHEN_TURN,
        })

    def test_smallblindlind_no_turn(self):
        h = history.History()
        l = "Siege 5: iflo_8 (petite blind) s'est couche. sur le Tournant"
        self.assertEquals(h.parse_line(l), {
            'player': 'iflo_8',
            'info': history.INFO_SMALL_BLIND,
            'win': history.WIN_LOOSE,
            'when': history.WHEN_TURN,
        })

    def test_bigblind_win(self):
        h = history.History()
        l = "Siege 6: pipao1 (grosse blind) a remporte (0.30)"
        self.assertEquals(h.parse_line(l), {
            'player': 'pipao1',
            'info': history.INFO_BIG_BLIND,
            'win': history.WIN_WIN,
            'when': history.WHEN_END,
        })

    def test_bigblind_no_flop(self):
        h = history.History()
        l = "Siege 1: genie001 (grosse blind) s'est couche. sur le Flop"
        self.assertEquals(h.parse_line(l), {
            'player': 'genie001',
            'info': history.INFO_BIG_BLIND,
            'win': history.WIN_LOOSE,
            'when': history.WHEN_FLOP,
        })

    def test_no_win_no(self):
        h = history.History()
        l = "Siege 4: TFC37 a remporte (0.08)"
        self.assertEquals(h.parse_line(l), {
            'player': 'TFC37',
            'info': history.INFO_NONE,
            'win': history.WIN_WIN,
            'when': history.WHEN_END,
        })

    def test_button_no_preflopwithout(self):
        h = history.History()
        l = "Siege 5: iflo_8 (bouton) s'est couche. avant Flop (n'a pas mise)"
        self.assertEquals(h.parse_line(l), {
            'player': 'iflo_8',
            'info': history.INFO_BUTTON,
            'win': history.WIN_LOOSE,
            'when': history.WHEN_PREFLOP_WITHOUT,
        })

    def test_smallblind_no_preflop(self):
        h = history.History()
        l = "Siege 6: pipao1 (petite blind) s'est couche. avant Flop"
        self.assertEquals(h.parse_line(l), {
            'player': 'pipao1',
            'info': history.INFO_SMALL_BLIND,
            'win': history.WIN_LOOSE,
            'when': history.WHEN_PREFLOP,
        })

    def test_bigblind_no_preflop(self):
        h = history.History()
        l = "Siege 2: agkiller69 (grosse blind) s'est couche. sur le Flop"
        self.assertEquals(h.parse_line(l), {
            'player': 'agkiller69',
            'info': history.INFO_BIG_BLIND,
            'win': history.WIN_LOOSE,
            'when': history.WHEN_FLOP,
        })

    def test_no_no_preflopwithout(self):
        h = history.History()
        l = "Siege 4: TFC37 s'est couche. avant Flop (n'a pas mise)"
        self.assertEquals(h.parse_line(l), {
            'player': 'TFC37',
            'info': history.INFO_NONE,
            'win': history.WIN_LOOSE,
            'when': history.WHEN_PREFLOP_WITHOUT,
        })

    def test_button_win_preflopwithout(self):
        h = history.History()
        l = "Siege 6: pipao1 (bouton) a remporte (0.17)"
        self.assertEquals(h.parse_line(l), {
            'player': 'pipao1',
            'info': history.INFO_BUTTON,
            'win': history.WIN_WIN,
            'when': history.WHEN_END,
        })


class TestHistoryPart(unittest.TestCase):

    def test_parts_count(self):
        h = history.History()
        count = sum([len(filter(None, [l for l in h.parse_part(p)]))
                     for p in h.get_parts()])
        self.assertEqual(count, 112)

    def test_part_0(self):
        h = history.History()
        self.assertEquals(h.get_parts()[0].split('*** SYNTHESE ***')[1], """
Pot total 0.32 | Commission 0.02
Tableau [5h 7s 3c Ts]
Siege 1: genie001 s'est couche. sur le Tournant
Siege 2: agkiller69 s'est couche. sur le Tournant
Siege 4: TFC37 (bouton) s'est couche. avant Flop (n'a pas mise)
Siege 5: iflo_8 (petite blind) s'est couche. sur le Tournant
Siege 6: pipao1 (grosse blind) a remporte (0.30)""")

    def test_parse_part_0(self):
        h = history.History()
        self.assertEquals([p for p in h.parse_part(h.get_parts()[0])], [
            {'info': 0, 'main': '93112556711', 'player': 'genie001', 'when': 3, 'win': 2},
            {'info': 0, 'main': '93112556711', 'player': 'agkiller69', 'when': 3, 'win': 2},
            {'info': 1, 'main': '93112556711', 'player': 'TFC37', 'when': 0, 'win': 2},
            {'info': 2, 'main': '93112556711', 'player': 'iflo_8', 'when': 3, 'win': 2},
            {'info': 3, 'main': '93112556711', 'player': 'pipao1', 'when': 5, 'win': 0}
        ])

    def test_part_1(self):
        h = history.History()
        self.assertEquals(h.get_parts()[1].split('*** SYNTHESE ***')[1], """
Pot total 0.09 | Commission 0.01
Tableau [2d 2c 9c]
Siege 1: genie001 (grosse blind) s'est couche. sur le Flop
Siege 2: agkiller69 s'est couche. avant Flop (n'a pas mise)
Siege 4: TFC37 a remporte (0.08)
Siege 5: iflo_8 (bouton) s'est couche. avant Flop (n'a pas mise)
Siege 6: pipao1 (petite blind) s'est couche. avant Flop""")

    def test_parse_part_1(self):
        h = history.History()
        self.assertEquals([p for p in h.parse_part(h.get_parts()[1])], [
            {'info': 3, 'main': '93112615401', 'player': 'genie001', 'when': 2, 'win': 2},
            {'info': 0, 'main': '93112615401', 'player': 'agkiller69', 'when': 0, 'win': 2},
            {'info': 0, 'main': '93112615401', 'player': 'TFC37', 'when': 5, 'win': 0},
            {'info': 1, 'main': '93112615401', 'player': 'iflo_8', 'when': 0, 'win': 2},
            {'info': 2, 'main': '93112615401', 'player': 'pipao1', 'when': 1, 'win': 2}
        ])

    def test_part_2(self):
        h = history.History()
        self.assertEquals(h.get_parts()[2].split('*** SYNTHESE ***')[1], """
Pot total 0.18 | Commission 0.01
Tableau [6s 2s 9d]
Siege 1: genie001 (petite blind) s'est couche. sur le Flop
Siege 2: agkiller69 (grosse blind) s'est couche. sur le Flop
Siege 4: TFC37 s'est couche. avant Flop (n'a pas mise)
Siege 5: iflo_8 s'est couche. avant Flop (n'a pas mise)
Siege 6: pipao1 (bouton) a remporte (0.17)""")

    def test_parse_part_2(self):
        h = history.History()
        self.assertEquals([p for p in h.parse_part(h.get_parts()[2])], [
            {'info': 2, 'main': '93112646958', 'player': 'genie001', 'when': 2, 'win': 2},
            {'info': 3, 'main': '93112646958', 'player': 'agkiller69', 'when': 2, 'win': 2},
            {'info': 0, 'main': '93112646958', 'player': 'TFC37', 'when': 0, 'win': 2},
            {'info': 0, 'main': '93112646958', 'player': 'iflo_8', 'when': 0, 'win': 2},
            {'info': 1, 'main': '93112646958', 'player': 'pipao1', 'when': 5, 'win': 0}
        ])

    def test_part_3(self):
        h = history.History()
        self.assertEquals(h.get_parts()[3].split('*** SYNTHESE ***')[1], """
Pot total 0.43 | Commission 0.03
Tableau [2d 8h 8c 6h 3h]
Siege 1: genie001 (bouton) s'est couche. sur le Tournant
Siege 2: agkiller69 (petite blind) s'est couche. avant Flop
Siege 4: TFC37 (grosse blind) a cache la main perdante. [8s Qd]
Siege 5: iflo_8 a montre [Qh Jh] et a gagne (0.40) avec une couleur, hauteur Dame
Siege 6: pipao1 s'est couche. avant Flop (n'a pas mise)""")

    def test_parse_part_3(self):
        h = history.History()
        self.assertEquals([p for p in h.parse_part(h.get_parts()[3])], [
            {'info': 1, 'main': '93112695597', 'player': 'genie001', 'when': 3, 'win': 2},
            {'info': 2, 'main': '93112695597', 'player': 'agkiller69', 'when': 1, 'win': 2},
            {'info': 3, 'main': '93112695597', 'player': 'TFC37', 'when': 5, 'win': 3},
            {'info': 0, 'main': '93112695597', 'player': 'iflo_8', 'when': 5, 'win': 1},
            {'info': 0, 'main': '93112695597', 'player': 'pipao1', 'when': 0, 'win': 2}
        ])

    def test_part_4(self):
        h = history.History()
        self.assertEquals(h.get_parts()[4].split('*** SYNTHESE ***')[1], """
Pot total 0.08 | Commission 0
Tableau [Kh 5c 4c 8h 3c]
Siege 1: genie001 s'est couche. sur le Riviere
Siege 2: agkiller69 (bouton) s'est couche. sur le Riviere
Siege 4: TFC37 (petite blind) a remporte (0.08)
Siege 5: iflo_8 (grosse blind) s'est couche. sur le Riviere
Siege 6: pipao1 s'est couche. avant Flop (n'a pas mise)""")

    def test_parse_part_4(self):
        h = history.History()
        self.assertEquals([p for p in h.parse_part(h.get_parts()[4])], [
            {'info': 0, 'main': '93112745577', 'player': 'genie001', 'when': 4, 'win': 2},
            {'info': 1, 'main': '93112745577', 'player': 'agkiller69', 'when': 4, 'win': 2},
            {'info': 2, 'main': '93112745577', 'player': 'TFC37', 'when': 5, 'win': 0},
            {'info': 3, 'main': '93112745577', 'player': 'iflo_8', 'when': 4, 'win': 2},
            {'info': 0, 'main': '93112745577', 'player': 'pipao1', 'when': 0, 'win': 2},
        ])

    def test_part_5(self):
        h = history.History()
        self.assertEquals(h.get_parts()[5].split('*** SYNTHESE ***')[1], """
Pot total 0.07 | Commission 0
Tableau [Qd Kh 4c]
Siege 1: genie001 s'est couche. sur le Flop
Siege 2: agkiller69 s'est couche. avant Flop (n'a pas mise)
Siege 4: TFC37 (bouton) a remporte (0.07)
Siege 5: iflo_8 (petite blind) s'est couche. avant Flop
Siege 6: pipao1 (grosse blind) s'est couche. sur le Flop""")

    def test_parse_part_5(self):
        h = history.History()
        self.assertEquals([p for p in h.parse_part(h.get_parts()[5])], [
            {'info': 0, 'main': '93112795753', 'player': 'genie001', 'when': 2, 'win': 2},
            {'info': 0, 'main': '93112795753', 'player': 'agkiller69', 'when': 0, 'win': 2},
            {'info': 1, 'main': '93112795753', 'player': 'TFC37', 'when': 5, 'win': 0},
            {'info': 2, 'main': '93112795753', 'player': 'iflo_8', 'when': 1, 'win': 2},
            {'info': 3, 'main': '93112795753', 'player': 'pipao1', 'when': 2, 'win': 2}
        ])

    def test_part_6(self):
        h = history.History()
        self.assertEquals(h.get_parts()[6].split('*** SYNTHESE ***')[1], """
Pot total 0.21 | Commission 0.01
Tableau [3s 2c 3d 5c Kc]
Siege 1: genie001 (grosse blind) s'est couche. sur le Riviere
Siege 2: agkiller69 s'est couche. avant Flop (n'a pas mise)
Siege 4: TFC37 s'est couche. avant Flop (n'a pas mise)
Siege 5: iflo_8 (bouton) a remporte (0.20)
Siege 6: pipao1 (petite blind) s'est couche. avant Flop""")

    def test_parse_part_6(self):
        h = history.History()
        self.assertEquals([p for p in h.parse_part(h.get_parts()[6])], [
            {'info': 3, 'main': '93112831616', 'player': 'genie001', 'when': 4, 'win': 2},
            {'info': 0, 'main': '93112831616', 'player': 'agkiller69', 'when': 0, 'win': 2},
            {'info': 0, 'main': '93112831616', 'player': 'TFC37', 'when': 0, 'win': 2},
            {'info': 1, 'main': '93112831616', 'player': 'iflo_8', 'when': 5, 'win': 0},
            {'info': 2, 'main': '93112831616', 'player': 'pipao1', 'when': 1, 'win': 2}
        ])

    def test_part_7(self):
        h = history.History()
        self.assertEquals(h.get_parts()[7].split('*** SYNTHESE ***')[1], """
Pot total 0.34 | Commission 0.02
Tableau [Qs 4h 9c 2d 8d]
Siege 1: genie001 (petite blind) s'est couche. sur le Riviere
Siege 2: agkiller69 (grosse blind) s'est couche. avant Flop
Siege 4: TFC37 s'est couche. sur le Riviere
Siege 5: iflo_8 a remporte (0.32)
Siege 6: pipao1 (bouton) s'est couche. sur le Riviere""")

    def test_parse_part_7(self):
        h = history.History()
        self.assertEquals([p for p in h.parse_part(h.get_parts()[7])], [
            {'info': 2, 'main': '93112877872', 'player': 'genie001', 'when': 4, 'win': 2},
            {'info': 3, 'main': '93112877872', 'player': 'agkiller69', 'when': 1, 'win': 2},
            {'info': 0, 'main': '93112877872', 'player': 'TFC37', 'when': 4, 'win': 2},
            {'info': 0, 'main': '93112877872', 'player': 'iflo_8', 'when': 5, 'win': 0},
            {'info': 1, 'main': '93112877872', 'player': 'pipao1', 'when': 4, 'win': 2}
        ])

    def test_part_8(self):
        h = history.History()
        self.assertEquals(h.get_parts()[8].split('*** SYNTHESE ***')[1], """
Pot total 0.39 | Commission 0.02
Tableau [4s 9d 7s 6s Qh]
Siege 1: genie001 (bouton) s'est couche. sur le Tournant
Siege 2: agkiller69 (petite blind) s'est couche. avant Flop
Siege 3: jvgap (grosse blind) a montre [Ad 8d] et a perdu avec Hauteur As
Siege 4: TFC37 a remporte (0.37)
Siege 5: iflo_8 s'est couche. avant Flop (n'a pas mise)
Siege 6: pipao1 s'est couche. avant Flop (n'a pas mise)""")

    def test_parse_part_8(self):
        h = history.History()
        self.assertEquals([p for p in h.parse_part(h.get_parts()[8])], [
            {'info': 1, 'main': '93112962501', 'player': 'genie001', 'when': 3, 'win': 2},
            {'info': 2, 'main': '93112962501', 'player': 'agkiller69', 'when': 1, 'win': 2},
            {'info': 3, 'main': '93112962501', 'player': 'jvgap', 'when': 5, 'win': 4},
            {'info': 0, 'main': '93112962501', 'player': 'TFC37', 'when': 5, 'win': 0},
            {'info': 0, 'main': '93112962501', 'player': 'iflo_8', 'when': 0, 'win': 2},
            {'info': 0, 'main': '93112962501', 'player': 'pipao1', 'when': 0, 'win': 2}
        ])

    def test_part_9(self):
        h = history.History()
        self.assertEquals(h.get_parts()[9].split('*** SYNTHESE ***')[1], """
Pot total 0.88 | Commission 0.05
Tableau [8d Qc 5h 8s Ac]
Siege 1: genie001 s'est couche. sur le Tournant
Siege 2: agkiller69 (bouton) s'est couche. sur le Flop
Siege 3: jvgap (petite blind) s'est couche. sur le Flop
Siege 4: TFC37 (grosse blind) s'est couche. sur le Flop
Siege 5: iflo_8 a remporte (0.83)
Siege 6: pipao1 s'est couche. sur le Riviere""")

    def test_parse_part_9(self):
        h = history.History()
        self.assertEquals([p for p in h.parse_part(h.get_parts()[9])], [
            {'info': 0, 'main': '93113015795', 'player': 'genie001', 'when': 3, 'win': 2},
            {'info': 1, 'main': '93113015795', 'player': 'agkiller69', 'when': 2, 'win': 2},
            {'info': 2, 'main': '93113015795', 'player': 'jvgap', 'when': 2, 'win': 2},
            {'info': 3, 'main': '93113015795', 'player': 'TFC37', 'when': 2, 'win': 2},
            {'info': 0, 'main': '93113015795', 'player': 'iflo_8', 'when': 5, 'win': 0},
            {'info': 0, 'main': '93113015795', 'player': 'pipao1', 'when': 4, 'win': 2}
        ])


class TestHistoryDb(unittest.TestCase):

    def test_simple_add(self):
        # init
        h = history.History()
        # create an item
        s = history.Hand(main='1234', player='iflo_8', info=1, when=5, win=1)
        h.session.add(s) 
        h.session.commit()
        # query and check
        s1 = h.session.query(history.Hand).filter_by(player='iflo_8').first()
        s2 = h.session.query(history.Hand).filter_by(main='1234').first()
        self.assertEqual(s1.id, s2.id)

    def test_update(self):
        h = history.History()
        # first pass
        h.update()
        self.assertEqual(h.get_hands().count(), 112)
        # no double
        h.update()
        self.assertEqual(h.get_hands().count(), 112)

    def test_update_0(self):
        h = history.History()
        # first pass
        h.update()
        q = h.get_hands(main='93112556711') 
        self.assertEqual(q.count(), 5)
        exp = [
            {'info': 0, 'main': '93112556711', 'player': 'genie001', 'when': 3, 'win': 2},
            {'info': 0, 'main': '93112556711', 'player': 'agkiller69', 'when': 3, 'win': 2},
            {'info': 1, 'main': '93112556711', 'player': 'TFC37', 'when': 0, 'win': 2},
            {'info': 2, 'main': '93112556711', 'player': 'iflo_8', 'when': 3, 'win': 2},
            {'info': 3, 'main': '93112556711', 'player': 'pipao1', 'when': 5, 'win': 0}
        ]
        for e in exp:
            hand = q.filter_by(player=e['player']).first()
            self.assertEqual(hand.info, e['info'])
            self.assertEqual(hand.when, e['when'])
            self.assertEqual(hand.win, e['win'])

    def test_update_1(self):
        h = history.History()
        # first pass
        h.update()
        q = h.get_hands(main='93112615401') 
        self.assertEqual(q.count(), 5)
        exp = [
            {'info': 3, 'main': '93112615401', 'player': 'genie001', 'when': 2, 'win': 2},
            {'info': 0, 'main': '93112615401', 'player': 'agkiller69', 'when': 0, 'win': 2},
            {'info': 0, 'main': '93112615401', 'player': 'TFC37', 'when': 5, 'win': 0},
            {'info': 1, 'main': '93112615401', 'player': 'iflo_8', 'when': 0, 'win': 2},
            {'info': 2, 'main': '93112615401', 'player': 'pipao1', 'when': 1, 'win': 2}
        ]
        for e in exp:
            hand = q.filter_by(player=e['player']).first()
            self.assertEqual(hand.info, e['info'])
            self.assertEqual(hand.when, e['when'])
            self.assertEqual(hand.win, e['win'])

    def test_update_2(self):
        h = history.History()
        # first pass
        h.update()
        q = h.get_hands(main='93112646958') 
        self.assertEqual(q.count(), 5)
        exp = [
            {'info': 2, 'main': '93112646958', 'player': 'genie001', 'when': 2, 'win': 2},
            {'info': 3, 'main': '93112646958', 'player': 'agkiller69', 'when': 2, 'win': 2},
            {'info': 0, 'main': '93112646958', 'player': 'TFC37', 'when': 0, 'win': 2},
            {'info': 0, 'main': '93112646958', 'player': 'iflo_8', 'when': 0, 'win': 2},
            {'info': 1, 'main': '93112646958', 'player': 'pipao1', 'when': 5, 'win': 0}
        ]
        for e in exp:
            hand = q.filter_by(player=e['player']).first()
            self.assertEqual(hand.info, e['info'])
            self.assertEqual(hand.when, e['when'])
            self.assertEqual(hand.win, e['win'])

    def test_update_3(self):
        h = history.History()
        # first pass
        h.update()
        q = h.get_hands(main='93112695597') 
        self.assertEqual(q.count(), 5)
        exp = [
            {'info': 1, 'main': '93112695597', 'player': 'genie001', 'when': 3, 'win': 2},
            {'info': 2, 'main': '93112695597', 'player': 'agkiller69', 'when': 1, 'win': 2},
            {'info': 3, 'main': '93112695597', 'player': 'TFC37', 'when': 5, 'win': 3},
            {'info': 0, 'main': '93112695597', 'player': 'iflo_8', 'when': 5, 'win': 1},
            {'info': 0, 'main': '93112695597', 'player': 'pipao1', 'when': 0, 'win': 2}
        ]
        for e in exp:
            hand = q.filter_by(player=e['player']).first()
            self.assertEqual(hand.info, e['info'])
            self.assertEqual(hand.when, e['when'])
            self.assertEqual(hand.win, e['win'])

    def test_stats(self):
        self.maxDiff = None
        # load data
        h = history.History()
        h.update()
        # check stats
        self.assertEquals(h.get_stats('genie001'), {
            'bigs': 4,
            'ends': 5,
            'hands': 21,
            'preflops': 18,
            'rivers': 8,
            'turns': 12,
            'wins': 4,
            'wins_end': 80.0,
            'wins_hand': 19.0,
            'wins_preflop': 22.0,
            'wins_river': 50.0,
            'wins_turn': 33.0,
            'bigs_preflop': 22.0,
        })
        self.assertEquals(h.get_stats('agkiller69'), {
            'bigs': 4,
            'ends': 2,
            'hands': 21,
            'preflops': 13,
            'rivers': 4,
            'turns': 5,
            'wins': 2,
            'wins_end': 100.0,
            'wins_hand': 10.0,
            'wins_preflop': 15.0,
            'wins_river': 50.0,
            'wins_turn': 40.0,
            'bigs_preflop': 31.0,
        })
        self.assertEquals(h.get_stats('TFC37'), {
            'bigs': 4,
            'ends': 7,
            'hands': 20,
            'preflops': 12,
            'rivers': 8,
            'turns': 8,
            'wins': 6,
            'wins_end': 86.0,
            'wins_hand': 30.0,
            'wins_preflop': 50.0,
            'wins_river': 75.0,
            'wins_turn': 75.0,
            'bigs_preflop': 33.0,
        })
        self.assertEquals(h.get_stats('iflo_8'), {
            'bigs': 3,
            'ends': 8,
            'hands': 21,
            'preflops': 14,
            'rivers': 9,
            'turns': 10,
            'wins': 5,
            'wins_end': 63.0,
            'wins_hand': 24.0,
            'wins_preflop': 36.0,
            'wins_river': 56.0,
            'wins_turn': 50.0,
            'bigs_preflop': 21.0,
        })
        self.assertEquals(h.get_stats('pipao1'), {
            'bigs': 3,
            'ends': 2,
            'hands': 16,
            'preflops': 9,
            'rivers': 4,
            'turns': 4,
            'wins': 2,
            'wins_end': 100.0,
            'wins_hand': 13.0,
            'wins_preflop': 22.0,
            'wins_river': 50.0,
            'wins_turn': 50.0,
            'bigs_preflop': 33.0,
        })

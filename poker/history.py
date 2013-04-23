# -*- coding: utf-8 -*-
import codecs
import re
import unicodedata

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext import declarative
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import UniqueConstraint


Base = declarative.declarative_base()
Session = sessionmaker()


class Hand(Base):

    __tablename__ = 'stories'
    __table_args__ = (
        UniqueConstraint('main', 'player'),
    )

    id = Column(Integer, primary_key=True)
    main   = Column(String)
    player = Column(String)
    info   = Column(Integer)
    when   = Column(Integer)
    win    = Column(Integer)

    def __init__(self, main=None, player=None, info=None, when=None, win=None):
        self.main = main
        self.player = player
        self.info = info
        self.when = when
        self.win = win

    def __repr__(self):
        return "<Hand(%s)>" % ', '.join([
            self.main,
            self.player,
            str(self.info),
            str(self.when),
            str(self.win),
        ]) 

# MAIN
RE_MAIN   = re.compile(r'^Main PokerStars No (\d{11})$')

# SIEGE/PLAYER
R_SIEGE   = r"^Siege \d{1}: ([a-zA-Z0-9_\-:.]*)"

# INFOS
R_INFO = [
    r"",
    r" \(bouton\)",
    r" \(petite blind\)",
    r" \(grosse blind\)",
]

[
    INFO_NONE,
    INFO_BUTTON,
    INFO_SMALL_BLIND,
    INFO_BIG_BLIND,
] = range(4)

# WIN/LOOSE
R_WIN = [
    r" a remporte \(\d*.\d*\)",
    r" a montre \[[a-zA-Z0-9]{2} [a-zA-Z0-9]{2}\] et a gagne \(\d*.\d*\)",
    r" s'est couche.",
    r" a cache la main perdante.",
    r" a montre",
]
# r" a montre \[[a-zA-Z0-9]{2} [a-zA-Z0-9]{2}\] et a perdu",
[
    WIN_WIN,
    WIN_WIN_SHOW,
    WIN_LOOSE,
    WIN_LOOSE_HIDE,
    WIN_LOOSE_SHOW,
] = range(5)

# WHEN
R_WHEN = [
    r" avant Flop \(n'a pas mise\)$",
    r" avant Flop$",
    r" sur le Flop$",
    r" sur le Tournant$",
    r" sur le Riviere$",
    r"",
]

[
    WHEN_PREFLOP_WITHOUT,
    WHEN_PREFLOP,
    WHEN_FLOP,
    WHEN_TURN,
    WHEN_RIVER,
    WHEN_END,
] = range(6)


class History(object):

    def __init__(self, db_conn='sqlite:///:memory:'):
        self.session = self.get_session(db_conn=db_conn)

    def get_session(self, db_conn='sqlite:///:memory:'):
        # create db
        engine = create_engine(db_conn)
        Base.metadata.create_all(engine)
        # init session
        Session.configure(bind=engine)
        return Session()

    def get_parts(self, path='./data/history.txt'):
        step = None
        main = None
        lines = list()
        with codecs.open(path, 'r', encoding='utf-8') as f:
            for l in f.readlines():
                l = unicodedata.normalize('NFD', l).encode('ascii', 'ignore')
                lines.append(l.strip())
        txt = '\n'.join(lines)
        return [p.strip() for p in txt.split('\n\n\n')]

    def parse_line(self, line):
        re_player = R_SIEGE
        for info, re_info in enumerate(R_INFO):
            for win, re_win in enumerate(R_WIN):
                for when, re_when in enumerate(R_WHEN):
                    _re_str = re_player + re_info + re_win + re_when
                    _re = re.compile(_re_str)
                    if _re.match(line):
                        return {
                            'player': _re.findall(line)[0],
                            'info': info,
                            'win': win,
                            'when': when,
                        }

    def parse_part(self, part):
        # part main
        main  = None
        # synthese flag
        synth = False
        # base query
        q = self.session.query(Hand)
        for i, l in enumerate(part.split('\n')):
            # get main nb
            if i == 0:
                l = l.split(':')[0].strip()
                main = RE_MAIN.findall(l)[0] if RE_MAIN.match(l)\
                                             else None
                # quit if already in db
                # or not found
                if not main\
                or q.filter_by(main=main).count():
                    # TODO log something if not main
                    # quit
                    yield None
            # update synth flag
            synth = synth or l.startswith('*** SYNTHESE ***')
            if not synth:
                continue
            # sige line ?
            _re = re.compile(R_SIEGE)
            if not _re.match(l):
                continue
            # manage synth lines
            hand = self.parse_line(l)
            if not hand:
                raise Exception('Not matched: `%s`' % l)
            # add main
            hand['main'] = main
            yield hand

    def update(self, path='./data/history.txt'):
        # quit
        quit = False
        for part in self.get_parts(path=path):
            for hand in self.parse_part(part):
                # update quit flag
                quit |= hand is None
                # quit cascade
                if quit:
                    break
                # store hand
                self.session.add(Hand(**hand))
            # quit cascade - continue
            if quit:
                break
        # commit - TODO may be catch double
        self.session.commit()

    def get_hands(self, **kw):
        q = self.session.query(Hand)
        return q.filter_by(**kw)

    def get_stats(self, player):
        stats = {
            'hands': 0,
            'wins': 0,
            'bigs': 0,
            'preflops': 0,
            'turns': 0,
            'rivers': 0, 
            'ends': 0, 
        }
        for hand in self.get_hands(player=player):
            stats['hands']    += 1
            stats['wins']     += 1 if hand.win in [WIN_WIN, WIN_WIN_SHOW]\
                                   else 0
            stats['bigs']     += 1 if hand.info == INFO_BIG_BLIND else 0
            stats['preflops'] += 1 if hand.when >= WHEN_PREFLOP   else 0
            stats['turns']    += 1 if hand.when >= WHEN_TURN      else 0
            stats['rivers']   += 1 if hand.when >= WHEN_RIVER     else 0
            stats['ends']     += 1 if hand.when == WHEN_END       else 0
        # additionnal stats
        # wins / hand
        stats['wins_hand'] = round(float(stats['wins'])*100/stats['hands'])
        # wins / preflop
        stats['wins_preflop'] = round(float(stats['wins'])*100/stats['preflops'])
        # wins / turn
        stats['wins_turn'] = round(float(stats['wins'])*100/stats['turns'])
        # wins / river
        stats['wins_river'] = round(float(stats['wins'])*100/stats['rivers'])
        # wins / end
        stats['wins_end'] = round(float(stats['wins'])*100/stats['ends'])
        # bigs / preflop
        stats['bigs_preflop'] = round(float(stats['bigs'])*100/stats['preflops'])
        # let's rock
        return stats

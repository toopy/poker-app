# -*- coding: utf-8 -*-
import json
import os

import logging
logger = logging.getLogger(__name__)

from functools import partial
from itertools import combinations

from twisted.internet.task import LoopingCall

from pycv.toolbox.image.config import Config
from pycv.toolbox.image.dictionary import Dictionary
from pycv.toolbox.image.position import Position as P
from pycv.toolbox.image.robot import Robot
from pycv.toolbox.image.size import Size as S


try:
    import pokereval
except Exception, e:
    logger.exception(e)
    pokereval = None


from west.socket.twisted.factory import SocketFactory

from poker import hand
from poker import table
from poker import history


NULL = [
    None,
    'nn',
    '_',
    'n',
]


class PokerDico(Dictionary):

    def __init__(self):
        Dictionary.__init__(self)
        # load poker values
        p_path = self.get_path('poker')
        self.pokervalues = []
        if os.path.exists(p_path):
            with open(p_path) as f:
                self.pokervalues = [l.strip() for l in f.readlines()]

    def find(self, box):
        val, result, neigh, dists = Dictionary.find(self, box) 
        # get corresponding poker value
        val = None if val is None or not val < len(self.pokervalues)\
                   else self.pokervalues[int(val)]
        # TODO add some debug
        # return expected values
        return val, result, neigh, dists

    def update(self, box, value):
        # keep the new str value
        if not value in self.pokervalues:
            self.pokervalues.append(value)
        # call parent with index as value
        Dictionary.update(self, box, self.pokervalues.index(value))

    def save(self):
        Dictionary.save(self)
        with open(self.get_path('poker'), 'w') as f:
            f.write('\n'.join(self.pokervalues))


class Pokerbot(Robot):

    def __init__(self, config, dico, zones):
        Robot.__init__(self, config=config, dico=dico, use_matrix=False)
        self._zones = zones

    def _key(self, val):
        return val

    def key_(self, val):
        return val

    def find_contours(self):
        for k, v in self._zones.iteritems():
            x, y, w, h = [abs(int(v[i])) for i in ['x', 'y', 'w', 'h']]
            yield (1920-x, y, w, h)

    def get_box(self, pos, size):
        p = P(1920 - pos.x, abs(pos.y))
        return self.threshold[p.y:p.y+size.h, p.x:p.x+size.w]

    def need_study(self, *args):
        return True

    def show_contours(self, pos, size, current=False, img=None): 
        return Robot.show_contours(self, pos, size, current=True, img=img)

    def preview(self): 
        Robot.preview(self)


class Zone(object):

    def __init__(self, x=None, y=None, w=None, h=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_pos(self):
        return P(self.x, self.y)

    def get_size(self):
        return S(self.w, self.h)

    def __str__(self):
        return '(%s,%s) (%s,%s)' % (self.x, self.y, self.w, self.h)


ROOT = os.path.join('poker', 'static', 'poker', 'resources', 'img', 'table')
STATIC = os.path.join('/fanstatic', 'poker', 'img', 'table')

IMG_LIST = [
    'table',
    'player_1_card_1',
    'player_1_card_2',
    'player_1_name',
    'player_2_cards',
    'player_2_name',
    'player_3_cards',
    'player_3_name',
    'player_4_cards',
    'player_4_name',
    'player_5_cards',
    'player_5_name',
    'player_6_cards',
    'player_6_name',
    'table_card_1',
    'table_card_2',
    'table_card_3',
    'table_card_4',
    'table_card_5',
]

CARD_KEYS = [
    'player_1_card_1',
    'player_1_card_2',
    'table_card_1',
    'table_card_2',
    'table_card_3',
    'table_card_4',
    'table_card_5',
]

CARD_OTHERS = [
    'player_2_cards',
    'player_3_cards',
    'player_4_cards',
    'player_5_cards',
    'player_6_cards',
]


class PokerSocketFactory(SocketFactory):

    def __init__(self, *args, **kwargs):
        SocketFactory.__init__(self, *args, **kwargs)


class PreviewTableFactory(SocketFactory):

    def __init__(self, *args, **kwargs):
        SocketFactory.__init__(self, *args, **kwargs)
        self.__config = Config()
        self.__dico = PokerDico()
        self.history = None
        self.robot = None

    def start(self):
        # init history with config
        self.history = history.History(
            conn=self.get_config('poker.conn'),
            path=self.get_config('poker.history')
        )
        # shortcut
        delay = self.get_config('poker.refresh')
        # not set
        if not delay:
            return
        # start loop
        try:
            LoopingCall(self.refresh).start(float(delay))
        except ValueError, e:
            pass

    def refresh(self):
        # update history
        self.history.update()
        # update clients
        for c in self.clients:
            self.message(c, '{}', refresh=True)

    def current_path(self, current, root=None):
        # split current
        current = None if not current\
                    else current.split('/')[-1].replace(')', '')
        # return root path
        return os.path.join(root, current) if root else current

    def next_path(self, current=None, root=None, ask='next'):
        # list available files
        files = os.listdir(ROOT)
        files.sort(reverse=True)
        # split current
        current = self.current_path(current)
        # get current pos
        index = 0 if not current in files else files.index(current)
        if ask == 'prev':
            index = len(files) - 1 if index == 0 else index - 1
        elif ask == 'next':
            index = 0 if index == len(files) - 1 else index + 1
        # add static path
        roots = [os.path.join(ROOT, f) for f in files]
        statics = [os.path.join(STATIC, f) for f in files]
        return roots[index], statics[index]

    def split_zone(self, key):
        value = self.get_config('poker.zone.%s' % key)
        return dict(zip(['x', 'y', 'w', 'h'], value.split()))

    def get_zones(self):
        return dict([(k, self.split_zone(k)) for k in IMG_LIST])

    def _info(self, key, value):
        # no robot
        if not self.robot:
            return
        # keep value
        # self.infos[key] = value
        # get key zone
        zone = Zone(**self.robot._zones[key])
        # update
        self.robot.remember(zone.get_pos(), zone.get_size(), value)

    def info_(self, key):
        # no robot
        if not self.robot:
            return ''
        # get key zone
        zone = Zone(**self.robot._zones[key])
        # get value
        return self.robot.get_value(zone.get_pos(), zone.get_size())

    def get_infos(self):
        return dict([(k, self.info_(k)) for k in IMG_LIST])

    def ev_cards(self, cards):
        for i, c in enumerate(cards):
            c = c.lower()
            for n in NULL[1:]:
                c = c.replace(n, '__')
            cards[i] = c
        return cards

    def get_eval(self, cards, me, others):
        # prepare pockets for eval
        pockets = [[str(c) for c in self.ev_cards(cards[:2])]]
        pockets += [['__', '__'] for o in others]
        if not pockets:
            return None
        # prepare board for eval
        board = [str(c) for c in self.ev_cards(cards[2:])]
        if not board:
            return None
        # get config iterations parameter
        iterations = self.get_config('eval.iterations')
        iterations = None if not iterations else int(iterations)
        # prepare kwargs
        kwargs = {
            'game': 'holdem',
            'pockets': pockets,
            'board': board,
        }
        if iterations:
            kwargs['iterations'] = iterations
        # debug
        logger.debug('k:%s' % kwargs)
        # eval
        try:
            _eval = pokereval.PokerEval().poker_eval(**kwargs)
            return  dict(zip([me] + others, [e['ev'] for e in _eval['eval']]))
        except Exception, e:
            logger.exception(e)

    def get_stats(self, infos):
        # no cards .. do nothin
        if not [k for k in CARD_KEYS[:2] if infos[k] not in NULL]:
            return {}
        # compute best hand
        cards = [infos[k] for k in CARD_KEYS\
                               if infos[k] not in NULL]
        hand_cls = hand.Hand if len(cards) > 2 else hand.HandPreflop
        if len(cards) > 2:
            hands = [hand_cls(*c).get_rank() for c in combinations(cards, r=5)]
            _hand = 0 if not hands else max(hands)
        else:
            _hand = hand_cls(*cards).get_rank()
        # get current turn
        board = [infos[k] for k in CARD_KEYS[2:]\
                               if infos[k] not in NULL]
        table_cls = table.Table(board)
        step = table_cls.get_step()
        # others
        me  = infos['player_1_name'] 
        oth = [infos[k.replace('cards', 'name')]
                     for k in CARD_OTHERS if infos[k] not in NULL]
        # players
        players = [me] + filter(None, oth)
        # eval
        _eval = self.get_eval(cards, me, oth)
        # stats
        _stats = dict([(p, self.history.get_stats(p, step)) for p in players])
        # res
        stats = {
            'hand': {'value': _hand, 'name': hand_cls.get_name(_hand)},
            'step': {'value': step, 'name': table_cls.get_name(step)},
            'evals': _eval,
            'stats': _stats,
        }
        return stats

    def message(self, client, msg, refresh=False):
        # DEBUG
        logger.debug('m:%s' % msg)
        # parse msg
        o = json.loads(msg)
        action = o.get('action')
        current = o.get('current')
        # action factory
        if action in ['next', 'prev'] or refresh:
            current, table_img = self.next_path(current=current, ask=action)
            # reset robot
            if self.robot:
                self.__dico.save()
            self.__config.path = current
            self.robot = Pokerbot(self.__config, self.__dico, self.get_zones())
            # get infos
            infos = self.get_infos()
            stats = self.get_stats(infos)
            resp = {
                'table_img': table_img,
                'zones': self.robot._zones,
                'infos': infos,
                'stats': stats,
            }
        elif action == 'form':
            k = o[action]
            self._info(k, o.get('value', ''))
            resp = {
                'msg': 'info `%s` updated.' % k
            }
        elif action == 'preview' and self.robot:
            self.robot.preview()
            resp = {
                'msg': 'previewing ...'
            }
        elif action == 'save' and self.robot:
            self.robot.dico.save()
            resp = {
                'msg': 'saved.'
            }
        else:
            resp = {
                'msg': 'unknown action: %s' % action
            }
        # DEBUG
        logger.debug('r:%s' % resp)
        # respond
        return self.send(client, json.dumps(resp))

    def send(self, client, msg):
        # default broadcast
        self.broadcast(msg)

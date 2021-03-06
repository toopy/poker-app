import logging
logger = logging.getLogger(__name__)


[
    NULL,
    PREFLOP,
    FLOP,
    TURN,
    RIVER
] = range(5)

NAMES = [
    '',
    'preflop',
    'flop',
    'turn',
    'river'
]

class Table(object):

    def __init__(self, board):
        self.board = board

    def get_step(self):
        nb_cards = len(self.board)
        if nb_cards == 0:
            return PREFLOP
        if nb_cards == 3:
            return FLOP
        if nb_cards == 4:
            return TURN
        if nb_cards == 5:
            return RIVER
        logger.debug('t:invalid board length:%s' % nb_cards)        
        return NULL

    @staticmethod
    def get_name(step):
        return '' if not step else NAMES[step]

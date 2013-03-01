import json
import os

import logging
logger = logging.getLogger(__name__)

from west.socket.twisted.factory import SocketFactory


KEY = "poker.app"

ROOT = os.path.join("poker", "static", "poker", "resources", "img", "table")
STATIC = os.path.join("/fanstatic", "poker", "img", "table")

IMG_LIST = [
    "table",
    "player_1_card_1",
    "player_1_card_2",
    "player_1_name",
    "player_2_cards",
    "player_2_name",
    "player_3_cards",
    "player_3_name",
    "player_4_cards",
    "player_4_name",
    "player_5_cards",
    "player_5_name",
    "player_6_cards",
    "player_6_name",
    "table_card_1",
    "table_card_2",
    "table_card_3",
    "table_card_4",
    "table_card_5",
]


class PokerSocketFactory(SocketFactory):

    def __init__(self, *args, **kwargs):
        SocketFactory.__init__(self, *args, **kwargs)


class PreviewTableFactory(SocketFactory):

    def __init__(self, *args, **kwargs):
        SocketFactory.__init__(self, *args, **kwargs)

    def current_path(self, current):
        # split current
        current = None if not current\
                    else current.split("/")[-1].replace(")", "")
        # return root path
        return os.path.join(ROOT, current)

    def next_path(self, current=None, root=None, ask="next"):
        # list available files
        files = os.listdir(ROOT)
        files.reverse()
        # split current
        current = None if not current\
                       else current.split("/")[-1].replace(")", "")
        # get current pos
        index = 0 if not current in files else files.index(current)
        if ask == "prev":
            index = len(files) - 1 if index == 0 else index - 1
        elif ask == "next":
            index = 0 if index == len(files) - 1 else index + 1
        # add static path
        files = [os.path.join(root, f) for f in files]
        return files[index]

    def split_zone(self, key):
        value = self.get_config("poker.zone.%s" % key)
        return dict(zip(["x", "y", "w", "h"], value.split()))

    def get_zones(self):
        return dict([(k, self.split_zone(k)) for k in IMG_LIST])

    def _info(self, zones, k, value, current=None):
        # ensure current
        current = self.current_path(current) if current\
                                             else self.next_path(root=ROOT)
        
        # DEBUG
        logger.debug("_i:%s:%s:%s" % (k, value, current))

    def info_(self, zones, k):
        return k

    def get_infos(self, zones):
        return dict([(k, self.info_(zones, k)) for k in IMG_LIST])

    def message(self, client, msg, refresh=False):
        # DEBUG
        logger.debug("msg: %s" % msg)
        # parse msg
        o = json.loads(msg)
        action = o.get("action")
        current = o.get("current")
        zones = self.get_zones()
        # action factory
        if action in ["next", "prev"] or refresh:
            infos = self.get_infos(zones)
            resp = {
                "table_img": self.next_path(current=current, ask=action,
                                            root=STATIC),
                "zones": zones,
                "infos": infos,
            }
        elif action == "form":
            k = o[action]
            self._info(zones[k], k, o.get("value", ""), current=current)
            resp = {
                "msg": "info `%s` updated!" % k
            }
        else:
            resp = {
                "msg": "unknown action: %s" % action
            }
        # default echo
        return self.send(client, json.dumps(resp))

    def send(self, client, msg):
        # default broadcast
        self.broadcast(msg)

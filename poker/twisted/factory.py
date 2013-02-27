import json
import os

import logging
logger = logging.getLogger(__name__)

from west.socket.twisted.factory import SocketFactory


KEY = "poker.app"


class PokerSocketFactory(SocketFactory):

    def __init__(self, *args, **kwargs):
        SocketFactory.__init__(self, *args, **kwargs)
        # TODO implement poker app loop


class PreviewTableFactory(SocketFactory):

    def __init__(self, *args, **kwargs):
        SocketFactory.__init__(self, *args, **kwargs)

    def get_image(self, current, ask="prev"):
        # static dir
        root = os.path.join("poker", "static", "poker", "resources", "img", "table")
        # list available files
        files = os.listdir(root)
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
        static = os.path.join("/fanstatic", "poker", "img", "table")
        files = [os.path.join(static, f) for f in files]
        return files[index]

    def split_zone(self, key):
        value = self.get_config("poker.zone.%s" % key)
        return dict(zip(["x", "y", "w", "h"], value.split()))

    def get_zones(self):
        return dict([(k, self.split_zone(k)) for k in [
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
        ]])

    def message(self, client, msg):
        o = json.loads(msg)
        action = o.get("action")
        if action in ["next", "prev"]:
            resp = {
                "table_img": self.get_image(o.get(action), action),
                "zones": self.get_zones()
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

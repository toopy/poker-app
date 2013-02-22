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
        static = os.path.join("/fanstatic", "poker", "img", "table")
        # list available files
        files = [os.path.join(static, f) for f in os.listdir(root)]
        files.reverse()
        # split current
        current = None if not current else current.split("/")[-1]
        # get current pos
        index = 0 if not current in files else files.index(current)
        if ask == "prev":
            index = len(files) - 1 if index == 0 else index - 1
        elif ask == "next":
            index = 0 if index == len(files) - 1 else index + 1
        return files[index]

    def message(self, client, msg):
        o = json.loads(msg)
        action = o.get("action")
        if action in ["next", "prev"]:
            resp = {
                "image_table_src": self.get_image(o.get(action), action)
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

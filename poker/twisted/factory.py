from west.twisted.factory import SocketFactory


class PokerSocketFactory(SocketFactory):

    def __init__(self, *args, **kwargs):
        SocketFactory.__init__(self, *args, **kwargs)
        # TODO implement poker app loop

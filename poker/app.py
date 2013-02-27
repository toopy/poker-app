from os import path as p

from webob import Response

from west.socket.app import SocketApp

K = "poker.app"

class PokerApp(SocketApp):
    
    def __init__(self, environ, **config):
        SocketApp.__init__(self, environ, **config)
        # url mapping
        self.connect("/static/{page}", action="page")
        self.connect("/static/table-img/{image}", action="table_img")

    def respond(self, environ, start_response):
        path = self.registry(environ, key=K)
        if path and p.exists(path):
            with open(path) as f:
                res = Response(body=f.read())
                return res(environ, start_response)
        return SocketApp.respond(self, environ, start_response)

    def page(self, environ, req, page=None, **kw):
        self.register(environ, K, p.join("static", page))

    def table_img(self, environ, req, image=None, **kw):
        self.register(environ, K, p.join("static", "table-img", image))

def poker_app_factory(environ, **config):
    return PokerApp(environ, **config)

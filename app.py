import cyclone.escape
import cyclone.web
import cyclone.websocket
import os.path
import sys
from twisted.python import log
from twisted.internet import reactor


class Application(cyclone.web.Application):
    def __init__(self):
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            autoescape=True,
        )

        handlers = [
            (r"/", MainHandler),
            (r"/echo", ChatSocketHandler),
        ]
        cyclone.web.Application.__init__(self, handlers, **settings)


class MainHandler(cyclone.web.RequestHandler):
    def get(self):
        self.render("base.html")

class ChatSocketHandler(cyclone.websocket.WebSocketHandler):
    clients = []

    def connectionMade(self):
        log.msg("connected!")
        self.clients.append(self)

    def messageReceived(self, message):
        log.msg("got message %s" % message)
        for client in self.clients:
            client.sendMessage(message)

    def connectionLost(self, *args, **kwargs):
        self.clients.remove(self)


def main():
    reactor.listenTCP(8888, Application())
    reactor.run()


if __name__ == "__main__":
    log.startLogging(sys.stdout)
    main()
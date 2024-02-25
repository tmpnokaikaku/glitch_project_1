# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.websocket
import os

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        WebSocketHandler.clients.add(self)
        print("WebSocket opened")

    def on_close(self):
        WebSocketHandler.clients.remove(self)
        print("WebSocket closed")

    def on_message(self, message):
        print("Received message: " + message)
        # クライアントにメッセージをエコーバック
        self.write_message("You said: " + message)

    @classmethod
    def send_updates(cls, message):
        for client in cls.clients:
            client.write_message(message)

    def check_origin(self, origin):
        return True  # すべてのオリジンからの接続を許可

application = tornado.web.Application([
    (r'/websocket', WebSocketHandler),
])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))  # Glitchで提供されるポートを使用
    application.listen(port)
    print("WebSocket server started\n")
    tornado.ioloop.IOLoop.instance().start()

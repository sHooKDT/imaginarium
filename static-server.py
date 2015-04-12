import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

import json

import logic

game_stage = 0
# 0 - Lobby
# 1 - Main turn
# 2 - Players turn
# 3 - Voting
# 4 - Score

static_path = 'W:/Projects/Imaginarium/client/'

class MainPageHandler(tornado.web.RequestHandler):
    def get(self):
        url = self.request.uri
        print(url)
        page = open(static_path + 'index.html', encoding='utf8').read()
        self.write(page)

class GameStarter(tornado.web.RequestHandler):
    def get(self):
        logic.start_game()

class UserSocketsHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print(self)

    def on_message(self, message):
        data = json.loads(message)
        if data['type'] == 'join':

            logic.new_player(data['data'], self)

            res = json.dumps({
                'type':'status',
                'id':len(logic.players),
                'data':len(logic.players)
            })
            self.write_message(res)

            for i in logic.players:
                mes = json.dumps({
                  'type':'status',
                  'data':'Another player joined'
                   })
                i['socket'].write_message(mes)

        else: print(data)

application = tornado.web.Application([
    (r"/startgame", GameStarter),
    (r"/", MainPageHandler),
    (r"/socket", UserSocketsHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {'path': static_path})
])

http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(8275)

tornado.ioloop.IOLoop.instance().start()

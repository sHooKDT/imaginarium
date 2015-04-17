import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

import json

import logic

from random import choice

game_stage = 0
# 0 - Lobby
# 1 - Main turn
# 2 - Players turn
# 3 - Voting
# 4 - Score

ready_count = 0
main_player = 0

static_path = 'W:/Projects/Imaginarium/client/'

"""def new_round():

        
        
        if logic.main_player != len(players)-1:
            logic.main_player += 1
        else: logic.main_player = 0"""

def all_ready():
    if game_stage == 1:
        if ready_count == 1: return True
        else: return False
    elif game_stage in [2, 3]:
        if ready_count == len(logic.players) - 1: return True
        else: return False
    else: return True
    
def change_stage(new_st):
    for player in logic.players:
        
        if players.index(player) == main_player:
            isMain = True
        else:
            isMain = False
        
        mes = json.dumps({
                'type': 'status',
                'stage': new_st,
                'hand': player.user_hand,
                'main': isMain,
                'table': [x.c_id for x in logic.table],
                'score': [x.score for x in logic.players]
            })

def indentify_client(id_socket):
    for player in logic.players:
        if player['socket'] == id_socket: return logic.players.index(player)
    return False

class MainPageHandler(tornado.web.RequestHandler):
    def get(self):
        url = self.request.uri
        print(url)
        page = open(static_path + 'index.html', encoding='utf8').read()
        self.write(page)

class GameStarter(tornado.web.RequestHandler):
    def get(self):
        print('Start game request received')
        change_stage(1)
    

class UserSocketsHandler(tornado.websocket.WebSocketHandler):
    
    global logic.cur_ass
    
    def open(self):
        print(self)

    def on_message(self, message):
        data = json.loads(message)
        client_id = identify_client(self)
        if data['type'] == 'choice':
            if game_stage == 1 and logic.players[main_player]['socket'] == self:
                logic.put_card(data['choice'])
                logic.cur_ass = data['data']
                change_stage(2)
        elif data['type'] == 'join':
            new_player(data['data'], self)

        else print('Incorrect request')

application = tornado.web.Application([
    (r"/startgame", GameStarter),
    (r"/", MainPageHandler),
    (r"/socket", UserSocketsHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {'path': static_path})
])

http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(8275)

tornado.ioloop.IOLoop.instance().start()

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

import json

import logic

from random import choice, randint
from time import sleep

game_stage = 0
# 0 - Lobby
# 1 - Main turn
# 2 - Players turn
# 3 - Voting
# 4 - Score

ready_count = 0

static_path = 'W:/Projects/Imaginarium/client/'

def all_ready():
    if game_stage == 1:
        if ready_count == 1: return True
        else: return False
    elif game_stage in [2, 3]:
        if ready_count == len(logic.players) - 1: return True
        else: return False
    else: return True
    
def change_stage(new_st):
    global ready_count
    global main_player
    global table
    
    ready_count = 0

    if new_st == 1: 
        if logic.main_player != len(logic.players)-1:
            logic.main_player += 1
        else: logic.main_player = 0
    elif new_st == 3:
        shuffle(logic.table)
    elif new_st == 4:
        logic.all_score(logic.main_player)

        
    for player in logic.players:
        
        if logic.players.index(player) == logic.main_player:
            isMain = True
        else:
            isMain = False
        
        mes = json.dumps({
                'type': 'status',
                'stage': new_st,
                'hand': player['user_hand'],
                'main': isMain,
                'table': [x['c_id'] for x in logic.table],
                'score': [x['score'] for x in logic.players]
            })
        player['socket'].write_message(mes)

def identify_client(id_socket):
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
    global cur_ass
    
    def open(self):
        print(self)

    def on_message(self, message):
        global ready_count
        data = json.loads(message)
        client_id = identify_client(self)
        if data['type'] == 'choice':
            if game_stage == 1 and logic.players[logic.main_player]['socket'] == self:
                logic.put_card(data['choice'], client_id)
                logic.cur_ass = data['data']
                change_stage(2)
            elif game_stage == 2:
                logic.put_card(data['choice'], client_id)
                ready_count += 1
                if all_ready(): change_stage(3)
            elif game_stage == 3:
                logic.vote(data['choice'], client_id)
                ready_count += 1
                if all_ready(): change_stage(4)
                sleep(randint(7, 13))
                if all_ready(): change_stage(1)
                    
        elif data['type'] == 'join':
            logic.new_player(data['data'], self)

        else: print('Incorrect request')

application = tornado.web.Application([
    (r"/startgame", GameStarter),
    (r"/", MainPageHandler),
    (r"/socket", UserSocketsHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {'path': static_path})
])

http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(8080)

tornado.ioloop.IOLoop.instance().start()

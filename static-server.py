# Includes
# Tornado
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
# JSON
import json
# Импорт игровой логики
import logic
# Extras
from random import choice, randint
from time import sleep

# Текущая стадия игры
game_stage = 0
# 0 - Lobby
# 1 - Main turn
# 2 - Players turn
# 3 - Voting
# 4 - Score

# Игроки в ожидании
ready_count = 0

# Полный путь до папки client
static_path = 'W:/Projects/Imaginarium/client/'

# Проверка готовности всех игроков на стадии
def all_ready():
    if game_stage == 1:
        if ready_count == 1: return True
        else: return False
    elif game_stage in [2, 3]:
        if ready_count == len(logic.players) - 1: return True
        else: return False
    else: return True

# Меняем стадию и рассылаем данные клиентам
def change_stage(new_st):
    global ready_count
    global main_player
    global table

    # Обнуляем готовность игроков
    ready_count = 0

    # Дополнительные действия для стадий
    if new_st == 1:
        if logic.main_player != len(logic.players)-1:
            logic.main_player += 1
        else: logic.main_player = 0
    elif new_st == 3:
        shuffle(logic.table)
    elif new_st == 4:
        logic.all_score(logic.main_player)

    # Рассылка текущих игровых данных
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

# Возвращает id игрока по сокеты клиента
def identify_client(id_socket):
    for player in logic.players:
        if player['socket'] == id_socket: return logic.players.index(player)
    return False

# Рассылка главной страницы
class MainPageHandler(tornado.web.RequestHandler):
    def get(self):
        print('Page request from ' + self.request.remote_ip)
        page = open(static_path + 'index.html', encoding='utf8').read()
        self.write(page)

# Обработчик запросов клиентов
class UserSocketsHandler(tornado.websocket.WebSocketHandler):
    global cur_ass

    def open(self):
        print('Websocket is ready.')

    def on_message(self, message):
        global ready_count
        data = json.loads(message)
        print(logic.players[identify_client(self)].name + ' is sending data: ' + data)
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
            print(data['data'] + ' is joining game.')
            logic.new_player(data['data'], self)
            if game_stage == 0:
                self.write_message(json.dumps({
                        'type': 'status',
                        'stage': 0
                    }))

        elif data['type'] == 'start':
            print('Someone is trying to start the game. Starting...')
            change_stage(1)

        else: print('Incorrect request')

application = tornado.web.Application([
    (r"/", MainPageHandler),
    (r"/socket", UserSocketsHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {'path': static_path})
])

http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(80)

tornado.ioloop.IOLoop.instance().start()

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
from random import choice, randint, shuffle
from time import sleep

# Текущая стадия игры
game_stage = 0
# 0 - Lobby
# 1 - Main turn
# 2 - Players turn
# 3 - Voting
# 4 - Score

# Счетчик раундов (в 1 надо раздать 6 карт, дальше - по 1)
round_num = 0

# Игроки в ожидании
ready_count = 0

# Относительный путь до папки с фронтендом
static_path = 'client/'

# Проверка готовности всех игроков на стадии
def all_ready():
    if game_stage == 1 and ready_count == 1: return True
    elif game_stage == 2 and ready_count == len(logic.players) - 1: return True
    elif game_stage == 3 and ready_count == len(logic.players): return True
    elif game_stage == 4: return True
    else: return False

# Меняем стадию и рассылаем данные клиентам
def change_stage(new_st):
    global ready_count
    global main_player
    global table
    global round_num
    global game_stage

    # Обнуляем готовность игроков
    ready_count = 0
    game_stage = new_st

    # Дополнительные действия для стадий
    if new_st == 1:

        print('---------ROUND ' + str(round_num) + ' STARTING---------')

        # Меняем главного игрока
        if logic.main_player != len(logic.players) - 1:
            logic.main_player += 1
        else:
            logic.main_player = 0

        print('Main player now is: ' + logic.players[logic.main_player]['name'])

        round_num += 1
        # Даем карты в зависимости от номера раунда
        if round_num == 1:
            logic.give_cards(6)
        else:
            logic.give_cards(1)

    # elif new_st == 2:
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
            'type': 'update',
            'state': {
                'stage': new_st,
                'hand': player['user_hand'],
                'main': isMain,
                'table': [x['c_id'] for x in logic.table],
                'score': [x['score'] for x in logic.players],
                'pcount': len(logic.players),
                'association': logic.cur_ass,
                'name': player['name']
            }
        })
        player['socket'].write_message(mes)
    print('...All players got data about new stage: ' + str(new_st))


# Возвращает id игрока по сокеты клиента
def identify_client(id_socket):
    for player in logic.players:
        if player['socket'] == id_socket: return logic.players.index(player)
    return False


# Рассылка главной страницы
class MainPageHandler(tornado.web.RequestHandler):
    def get(self):
        print('Connection with ip: ' + self.request.remote_ip)
        page = open(static_path + 'index.html', encoding='utf8').read()
        self.write(page)


# Обработчик запросов клиентов
class UserSocketsHandler(tornado.websocket.WebSocketHandler):
    global cur_ass

    def open(self):
        print('Websocket connected.')
        # Посылаем информацию о лобби
        self.write_message(json.dumps({
            'type': 'update',
            'state': {
                'stage': 0,
                'hand': [],
                'main': False,
                'table': [],
                'score': [],
                'pcount': len(logic.players),
                'association': '',
                'name': ''
            }
        }))

    def on_message(self, message):
        global ready_count
        global game_stage
        data = json.loads(message)
        # print(logic.players[identify_client(self)].name + ' is sending data: ' + data)
        client_id = identify_client(self)
        if data['type'] == 'choice':
            print('Choice from ' + logic.players[identify_client(self)]['name'])
            # if game_stage == 1 and logic.players[logic.main_player]['socket'] == self:
            if game_stage == 1:
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
                if all_ready(): 
                    logic.all_score(logic.main_player)
                    logic.done_cards()
                    change_stage(4)
                    sleep(randint(7, 13))
                    change_stage(1)

        elif data['type'] == 'join':
            print(data['data'] + ' is joining game.')
            logic.new_player(data['data'], self)
            if game_stage == 0:
                self.write_message(json.dumps({
                    'type': 'update',
                    'state': {
                        'stage': 0,
                        'hand': [],
                        'main': False,
                        'table': [],
                        'score': [],
                        'pcount': len(logic.players),
                        'association': '',
                        'name': ''
                    }
                }))

        elif data['type'] == 'start':
            print('Someone is trying to start the game. Starting...')
            change_stage(1)

        else:
            print('Incorrect request')


application = tornado.web.Application([
    (r"/", MainPageHandler),
    (r"/socket", UserSocketsHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {'path': static_path})
])

http_server = tornado.httpserver.HTTPServer(application)

server_port = 80
print('Imaginarium game server started on port: ' + str(server_port))
http_server.listen(server_port)
tornado.ioloop.IOLoop.instance().start()

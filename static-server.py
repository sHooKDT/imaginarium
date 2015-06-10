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
import random
from time import sleep

# Текущая стадия игры
game_stage = 0
# 0 - Lobby
# 1 - Main turn
# 2 - Players turn
# 3 - Voting
# 4 - Score
# 5 - Winner

# Счетчик раундов (в 1 надо раздать 6 карт, дальше - по 1)
round_num = 0

# Победный счет
win_score = 4
isWon = False

# Игроки в ожидании
ready_count = 0

# Относительный путь до папки с фронтендом
static_path = 'client/'

# Проверка готовности всех игроков на стадии
def all_ready():
    if game_stage == 1 and ready_count == 1:
        return True
    elif game_stage == 2 and ready_count == len(logic.players) - 1:
        return True
    elif game_stage == 3 and ready_count == len(logic.players) - 1:
        return True
    elif game_stage == 4:
        return True
    else:
        return False

# Проверка наличия победителя
def check_win():
    global isWon
    for player in logic.players:
        if player['score'] >= win_score:
            print('We have a winner - ' + player['name'])
            change_stage(5)
            isWon = True

# Отсылаем текущее состояние игры
def notify_all():
    for player in logic.players:

        if logic.players.index(player) == logic.main_player:
            isMain = True
        else:
            isMain = False

        mes = json.dumps({
            'type': 'update',
            'state': {
                'stage': game_stage,
                'hand': player['user_hand'],
                'main': isMain,
                'table': [x['c_id'] for x in logic.table if x['owner']!=logic.players.index(player)],
                'pcount': len(logic.players),
                'association': logic.cur_ass,
                'name': player['name']
            }
        })

        player['socket'].write_message(mes)

# Посылаем всем текущий счет (вызывается при переходе на страницу счета)
def send_score():
    score_table = []
    for player in logic.players:
        plid = logic.players.index(player)
        pvote = 0
        pturn = 0
        pmain = False
        for card in logic.table:
            if card['owner'] == plid:
                pturn = card['c_id']
            for vote in card['votes']:
                if vote == plid:
                    pvote = card['c_id']
        if plid == logic.main_player:
            pmain = True
        else:
            pmain = False
        score_table.append({
            'name': player['name'],
            'vote': pvote,
            'turn': pturn,
            'score': player['score'],
            'main': pmain
        })

    for player in logic.players:
        player['socket'].write_message(json.dumps({
            'type': 'score',
            'score': score_table
        }))

# Меняем стадию и рассылаем данные клиентам
def change_stage(new_st):
    global ready_count
    global round_num
    global game_stage

    # Обнуляем готовность игроков
    ready_count = 0
    game_stage = new_st

    # Дополнительные действия для стадий
    if new_st == 1:
        round_num += 1

        print('---------ROUND ' + str(round_num) + ' STARTING---------')

        # Даем карты в зависимости от номера раунда
        if round_num == 1:
            logic.give_cards(6)
            # Рандомно выбираем ведущего
            logic.main_player = logic.players.index(random.choice(logic.players))
        else:
            logic.give_cards(1)

        # Меняем главного игрока
        if logic.main_player != len(logic.players) - 1:
            logic.main_player += 1
        else:
            logic.main_player = 0

        logic.done_cards()
        # Обнуляем ассоциацию
        logic.cur_ass = ''

        print('Main player: ' + logic.players[logic.main_player]['name'])

    # elif new_st == 2:
    elif new_st == 3:
        random.shuffle(logic.table)
    elif new_st == 4:
        logic.all_score(logic.main_player)
        send_score()
        check_win()

    # Рассылка текущих игровых данных
    notify_all()

    print('### Stage changed to: ' + str(new_st))

    if (new_st == 4) & (isWon == False):
        sleep(10)
        change_stage(1) 

# Запускаем новую игру
def new_game():
    global round_num, game_stage, ready_count, isWon
    print('New game starting...')
    # Обнуление состояний
    round_num = 0
    game_stage = 0
    ready_count = 0
    isWon = False
    # Обнуление логики
    logic.reinitialise()
    change_stage(1)

# Возвращает id игрока по сокеты клиента
def identify_client(id_socket):
    for player in logic.players:
        if player['socket'] == id_socket: return logic.players.index(player)
    return False

# Рассылка главной страницы
class MainPageHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        print('Connection with ip: ' + self.request.remote_ip)
        page = open(static_path + 'index.html', encoding='utf8').read()
        self.write(page)


# Обработчик запросов клиентов
class UserSocketsHandler(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk):
        pass

    def open(self):
        print('Websocket connected.')
        # Посылаем информацию о лобби
        self.write_message(json.dumps({
            'type': 'update',
            'state': {
                'stage': game_stage,
                'hand': [],
                'main': False,
                'table': [],
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
            print('________got mes from ' + logic.players[identify_client(self)]['name'])
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
                if all_ready(): change_stage(4)

        elif data['type'] == 'join':
            print(data['data'] + ' is joining game.')
            logic.new_player(data['data'], self)
            notify_all()

        elif data['type'] == 'start':
            new_game()

        else:
            print('Incorrect request')

# Инициализация и запуск сервера
application = tornado.web.Application([
    (r"/", MainPageHandler),
    (r"/socket", UserSocketsHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {'path': static_path})
])

http_server = tornado.httpserver.HTTPServer(application)

server_port = 27777
print('Imaginarium game server started on port: ' + str(server_port))
http_server.listen(server_port)
tornado.ioloop.IOLoop.instance().start()

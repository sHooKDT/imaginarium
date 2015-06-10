# Includes
import random

# Globals
cards = []
players = []
table = []
cur_ass = ''
used_cards = []
main_player = 0

# Обнуление логического состояния игры
def reinitialise():
    global cards, main_player, used_cards, cur_ass, table, players
    main_player = 0
    cards = random.sample(range(920), 120)
    print('Cards for this game:')
    print('<%s>' % ', '.join(map(str, cards)))
    used_cards = []
    cur_ass = ''
    table = []
    for player in players:
        player['score'] = 0
        player['user_hand'] = []

# Создаем нового игрока с именем x и сокетом y
def new_player(name, self):
    players.append({
        "name": name,
        "score": 0,
        "user_hand": [],
        "socket": self
    })


# Раздаем всем игрокам по x карт
def give_cards(cards_num):
    for player in players:
        for x in range(cards_num):
            player['user_hand'].append(cards.pop(random.randint(0, len(cards) - 1)))


# Выкладываем карту из руки на стол
def put_card(card_id, user_id):
    table.append({
        "c_id": players[user_id]["user_hand"].pop(card_id),
        "owner": user_id,
        "votes": []
    })


# Засчитываем голос игрока
def vote(card_id, user_id):
    table[card_id]['votes'].append(user_id)


# Подсчитываем очки
def all_score(main_player):
    for card in table:
        votes = card['votes']
        if card['owner'] == main_player:
            if votes == []:
                players[main_player]['score'] -= 2
            elif len(votes) == len(players) - 1:
                players[main_player]['score'] -= 3
            else:
                players[main_player]['score'] +=3
                for user_id in votes:
                  players[user_id]['score'] += 3
                  players[main_player]['score'] += 1
        else:
            for user_id in votes:
              players[card['owner']]['score'] += 1


# Бита
def done_cards():
    global table
    global cards
    global used_cards
    for x in table:
        used_cards.append(x['c_id'])
    table = []
    if not cards:
        for i in used_cards:
            cards.append(i)
        used_cards = []

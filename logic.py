# Includes
from random import random,randint,shuffle

# Globals
cards = [x for x in range(63)]
players = []
table = []
cur_ass = ''
used_cards = []
main_player = 0

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
           player['user_hand'].append(cards.pop(randint(0,len(cards)-1)))

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
        if card['owner'] == main_player:
            a = card['votes'] # проголосовавшие за ведущего
            if a == []:
                players[main_player]['score']-=3
                if players[main_player]['score']<0:
                  players[main_player]['score']=0
            # TODO: elif all for main then main -= 3???
            else:
               for user_id in a:
                   print('Player',user_id,', right choice')
                   players[user_id]['score']+=3
                   players[main_player]['score']+=1
        else:
            players[card['owner']]['score']+=1

# Бита
def done_cards():
    global table
    global cards
    global used_cards
    for x in table:
        used_cards.append(x['c_id'])
    table = []
    if cards == []:
        for i in used_cards:
            cards.append(i)
        used_cards = []

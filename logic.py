#Includes
from random import random,randint,shuffle

#Globals
cards = [x for x in range(63)]
players = []
table = []
cur_ass = ''
used_cards = []
main_player = 0

#Создаем нового игрока с именем x
def new_player(name, self):
    players.append({
            "name": name,
            "score": 0,
            "user_hand": [],
            "socket": self
        })
    print(name + ' joined game.')

#Даем всем игрокам по x карт
def give_cards(cards_num):
    for player in players:
        for x in range(cards_num):
           player['user_hand'].append(cards.pop(randint(0,len(cards)-1)))

#Выкладываем карту из руки на стол
def put_card(card_id, user_id):
    table.append({
        "c_id": players[user_id]["user_hand"].pop(card_id),
        "owner": user_id,
        "votes": []
        })

#Даем ход игроку
def let_turn(user_id, isMain):
    global cur_ass
    if isMain == False:
        print('Current association: ', cur_ass)
    print('Player ', players[user_id]['name'], ', choose your card: ', players[user_id]["user_hand"])
    chosen_card = int(input())
    
    if isMain:
        print('Write your association: ')
        cur_ass = input()
    return chosen_card

#Голосование
def vote(card_id, user_id):
    table[card_id]['votes'].append(user_id)

#Подсчитываем очки
def all_score(main_player):
    for card in table:
        if card['owner'] == main_player:
           a = card['votes'] # проголосовавшие за ведущего
           if a == []:
               players[main_player]['score']-=3
               if players[main_player]['score']<0:
                   players[main_player]['score']=0
           else:
               for user_id in a:
                   print('Player',user_id,', right choice')
                   players[user_id]['score']+=3
                   players[main_player]['score']+=1
        else:
            players[card['owner']]['score']+=1

#Бита
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
           
 
    
    
#Стартуем игру в цикле
def start_game():
    Winner = False
    main_player = 0

    give_cards(6)
    
    while Winner == False :
        global table
        #Ход главного игрока
        put_card(let_turn(main_player, True), main_player)

        #Массив всех остальных
        array_players=[x for x in range(0,len(players))]
        array_players.remove(main_player)

        #Все ходят
        for i in array_players:
           put_card(let_turn(i, False), i)

        #Шафл стола
        shuffle(table)

        #Покажем стол
        print('Table: ', end="")
        for i in table:
            print(i['c_id'], end =" ")
        print()

        #Пускаем голосование
        all_vote(main_player)

        #Подсчёт очков
        all_score(main_player)
            
        #done_cards
        done_cards()
        
        #Даем всем по карте
        give_cards(1)

        #Меняем главного
        if main_player != len(players)-1:
            main_player += 1
        else: main_player = 0

        for i in range(len(players)):
            if players[i]['score'] >= 15:
                Winner = True

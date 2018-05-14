# coding: utf-8
from __future__ import unicode_literals
import json



# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):
    #response.user_id
    if request.is_new_session:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        with open('map.json') as maps:
            mapaa = json.load(maps)["maps"]
        user_storage = {
            "user_id":request.user_id,
            "maps":mapaa,
            "human" : 1,
            "AliceTurns":[],
            "userMatrix":[]
            #TODO map generate
            
        }

        # buttons, user_storage = get_suggests(user_storage)
        response.set_text('Привет! Играем в морской бой. Для атаки введите координаты ввиде (А1)!')
        # response.set_buttons(buttons)

        return response, user_storage

    # Обрабатываем ответ пользователя.
    if request.command.lower() in ['убил', 'ранил', 'попал', 'мимо']:
        if request.command.lower() == 'убил':
            if ifend(user_storage["maps"]):
               # print(user_storage)
                if user_storage["human"]==1:
                    response.set_text('Конец игры. Человек победил.')

                else:
                    response.set_text('Конец игры. Алиса победила.')
            else:
                a = ''
                #response.set_text('Я хожу')
                alph = 'абвгдежзийкл'
                user_storage["human"] = 0
                c = AliceTurn(user_storage)

                a = a + ' Я хожу ' + alph[c[0]].upper() + str(c[1] + 1)
                response.set_text(a)
        if request.command.lower() in ['ранил', 'попал']:
            user_storage["human"]  = 0;
            t = AliceTurn(user_storage)
            alph = 'абвгдежзийкл'
            a = 'Я хожу ' + alph[t[0]].upper() + str(t[1] + 1)
            response.set_text(a)

        if request.command.lower() == 'мимо':
           # print(user_storage)
            response.set_text('Ваш ход')
            user_storage["human"] = 1
        return response, user_storage
    elif request.command.lower()[0] in 'абвгдежзийкл' and request.command.lower()[1:] in '12345678910' and user_storage["human"] == 1 and int(request.command.lower()[1:])<10:

        a = vustrel(user_storage["maps"],request.command.lower())
        if a == 'мимо':
            alph = 'абвгдежзийкл'
            user_storage["human"] = 0
            c = AliceTurn(user_storage)

            a = a + 'Я хожу ' +alph[c[0]].upper() +str(c[1]+1)
        else:
            user_storage["human"] = 1
        response.set_text(a)

        return response, user_storage
    elif user_storage["human"] == 0:
        t = AliceTurn(user_storage)
        alph = 'абвгдежзийкл'
        a =  'Я хожу ' + alph[t[0]].upper() + str(t[1] + 1)
        response.set_text(a)

        user_storage["human"] = 1;
        return response, user_storage
    else:
        response.set_text("Некорректная команда")
        return response, user_storage

def AliceTurn(user_storage):
    if user_storage["userMatrix"]==[]:
        user_storage["userMatrix"] = [[0 for j in range(10)] for i in range(10)]
    import random
    def generateTurn():
        turn = [random.randint(0,9),random.randint(0,9)]
        return turn
    turn = generateTurn()
    i = 0
    while user_storage["userMatrix"][turn[0]][turn[1]] != 0:
        i += 1;
        turn = generateTurn()
        if i==100:
            turn = [-1,-1]
    user_storage["userMatrix"][turn[0]][turn[1]] = 2;
    return turn


def ifend(matrix):
    end = True
    for i in matrix:
        if 1 in i:
            end = False
            return end
    return end




def vustrel(matrix, coord):
    k=0
    alph = 'абвгдежзийкл'
    output = None
    list_ship = []
    for j in range(len(alph)):
        if coord[0]==alph[j]:
            k = j

    ind = int(coord[1])-1
    print(matrix[ind][k])
    if matrix[ind][k]==2:
        print('ok1')
        output = 'уже'
    elif matrix[ind][k]==0:
        output = 'мимо'
        print('ok2')
    elif matrix[ind][k] == 1:
        print('ok3')
        matrix[ind][k] = 2

        if matrix[ind][k+1]==0 and matrix[ind][k-1]==0 and matrix[ind+1][k]==0 and matrix[ind-1][k]==0:
            output = 'убит'
        elif matrix[ind][k+1]==0 and matrix[ind][k-1]==0:
            for j in range(4):
                if j>=0 and j<=9:
                    if matrix[ind+j][k]==0:
                        break
                    else:
                        list_ship.append(matrix[ind+j][k])
            for j in range(1,5):
                if j>=0 and j<=9:
                    if matrix[ind-j][k]==0:
                        break
                    else:
                        list_ship.append(matrix[ind-j][k])
        elif matrix[ind+1][k]==0 and matrix[ind-1][j]==0:
            for j in range(1, 5):
                if j >= 0 and j <= 9:
                    if matrix[ind][k+j]==0:
                        break
                    else:
                        list_ship.append(matrix[ind][k+j])
            for j in range(1,5):
                if j >= 0 and j <= 9:
                    if matrix[ind][k-j]==0:
                        break
                    else:
                        list_ship.append(matrix[ind][k-j])

        if 1 in list_ship:
            output = 'ранен'
        else:
            output = 'убит'
    return output

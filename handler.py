# coding: utf-8
from __future__ import unicode_literals
from json import dump
from random import randint, choice
from copy import deepcopy
from re import findall, match


SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
ALPHABET = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и']


# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):
    # response.user_id
    if request.is_new_session:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        ship_battle = ShipBattle()
        ship_battle.place_SHIPS()        
        
        user_storage = {
            "user_id": request.user_id,
            "humans_turn": True,
            "life": sum(SHIPS),
            "AliceTurns": [],
            "Alices_matrix": ship_battle.field,
            "users_matrix": [[0 for j in range(10)] for i in range(10)],
            "sinked_ship": [],
            "cheating_stage": 0
        }

        # buttons, user_storage = get_suggests(user_storage)
        response.set_text('Привет! Играем в морской бой. Каждая клетка обозначается алфавитной буквой по горизонтали '
                          '(от "А" до "И" слева направо) и цифрой по вертикали (от 1 до 10 сверху вниз). Мои корабли уже расставлены. '
                          'По вашей готовности атакуйте. Чтобы провести атаку скажите или введите координаты.')
        # response.set_buttons(buttons)
        return response, user_storage

    killed = ['убила', 'убил', 'потопила', 'потоплен', 'потопил']
    injured = ['попала', 'попал', 'попадание', 'ранил', 'ранила']
    missed = ['мимо', 'промах', 'промазала', 'промазал']
    words = ['убила', 'убил', 'потопила', 'потопил', 'потоплен', 'попала', 'попал', 'попадание', 'ранил', 'ранила',
             'мимо',
             'промах', 'промазала', 'промазал']

    phrases_for_alices_turn = ['Пожалуйста, не жульничайте, я контролирую игру.', 'Помоему, сейчас не ваш ход.',
                               'Со мной такое не прокатит. Сейчас мой ход.', 'Может вы не будете меня обманывать?',
                               'Давайте я забуду это, а вы ответите еще раз.']

    phrases_for_humans_turn = ['Сейчас ваш ход, не надо поддаваться.',
                               'Может вы что-то перепутали? Сейчас вы атакуете.',
                               'Я конечно не против, но давайте играть по правилам', 'Не люблю лёгкие победы...']

    # Обрабатываем ответ пользователя.
    user_message = request.command.lower().strip().replace(' ', '')

    try_to_make_coor = ''.join(findall(r'\w+', user_message))
    matched = match('\w\d0*', try_to_make_coor)

    # Если ходит Алиса
    if user_message in words:
        if not user_storage["humans_turn"]:
            if user_message in killed:
                print(AliceTurn(user_storage["users_matrix"], killed=True))

            elif user_message in injured:
                print(AliceTurn(user_storage["users_matrix"], killed=False))

            elif user_message in missed:
                user_storage["humans_turn"] = True
                print('Ваш ход.')

        # Если игрок сказал не в свой ход
        print(choice(phrases_for_humans_turn))

    # Если ходит игрок
    elif matched is not None:
        if user_storage["humans_turn"]:
            letter = matched.group(0)[0]
            number = int(matched.group(0)[1:])
            if 0 < number < 11 and letter in ALPHABET:
                result_of_fire = fire(user_storage["Alices_matrix"], (ALPHABET.index(letter), number - 1))

                if result_of_fire == 'Мимо':
                    user_storage["humans_turn"] = False
                    print('Мимо. Я хожу. ' + AliceTurn(user_storage['users_matrix'], killed=False))

                else:
                    user_storage["humans_turn"] = True
                    user_storage["life"] -= 1

                    print(result_of_fire)
            else:
                print("Координаты клетки обозначаются буквой (от А до И) и числом (от 1 до 10) для поля "
                      "10 на 10 клеток. Пример - А1.")
        else:
            print(choice(phrases_for_alices_turn))


    # elif not user_storage["humans_turn"] == 0:
    #     t = AliceTurn(user_storage)
    #     alph = 'абвгдежзийкл'
    #     a = 'Я хожу ' + alph[t[0]].upper() + str(t[1] + 1)
    #     print(a)
    #     user_storage["humans_turn"] = 1
    #     return response, user_storage
    else:
        print("Простите, но я вас не поняла.")


def AliceTurn(matrix, killed=False):
    # if len(user_storage["sinked_ship"]) == 0:
    #     possible_cells = []
    #     for y in range(10):
    #         for x in range(10):
    #             if user_storage["userMatrix"][y][x] == 0:
    #                 pass
    #
    #     possible_cells = list(filter(lambda x,y: user_storage["userMatrix"][y][x] == 0, []))
    #     turn = [random.randint(0, 9), random.randint(0, 9)]
    # else:
    #     pass
    # TODO сделать обработку убил\ранил
    i = 0
    turn = [randint(0, 9), randint(0, 9)]
    while matrix[turn[1]][turn[0]] != 0:
        i += 1
        turn = [randint(0, 9), randint(0, 9)]
        if i >= 120:
            turn = [-1, -1]
    matrix[turn[1]][turn[0]] = 1

    return "{}{}".format(ALPHABET[turn[0]].upper(), turn[1] + 1)


# def ifend(matrix):
#     end = True
#     for i in matrix:
#         if 1 in i:
#             end = False
#             return end
#     return end


# 1 - целые корабли, 2 - клетки, куда стреляли
def fire(matrix, coord):
    x, y = coord
    if matrix[y][x] == 2 or matrix[y][x] == 3:
        output = 'Вы уже стреляли сюда'
    elif matrix[y][x] == 0:
        output = 'Мимо'
        matrix[y][x] = 2
    elif matrix[y][x] == 1:
        matrix[y][x] = 3
        ship = [(x, y)]
        was = []
        while len(ship) > 0:
            sinking = True
            x, y = ship.pop(0)
            was.append((x, y))
            possibleCells = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            for possible in possibleCells:
                if -1 < x + possible[0] < 10 and -1 < y + possible[1] < 10:
                    if (x + possible[0], y + possible[1]) not in was:
                        if matrix[y + possible[1]][x + possible[0]] == 3:
                            ship.append((x + possible[0], y + possible[1]))
                        elif matrix[y + possible[1]][x + possible[0]] == 1:
                            sinking = False
                            break
            if sinking:
                for cell in was:
                    matrix[cell[1]][cell[0]] = 2
                output = 'Потоплен'
            else:
                output = 'Ранен'

    return output


class ShipBattle:
    def __init__(self):
        self.reversed_alphabet = {j: i for i, j in enumerate(ALPHABET)}
        self.field = [[0 for i in range(10)] for i in range(10)]

    def check_cell(self, cell, first_cell=False):
        x, y = cell
        count = 0
        possibleCells = [(1, 1), (-1, -1), (0, 1), (1, 0), (-1, 0), (0, -1), (-1, 1), (1, -1)]
        for possible in possibleCells:
            if -1 < x + possible[0] < 10 and -1 < y + possible[1] < 10:
                if self.field[y + possible[1]][x + possible[0]] == 1:
                    count += 1

        if (count < 2 and not first_cell) or (first_cell and count == 0):
            return True
        return False

    def place_SHIPS(self):
        for ship in SHIPS:
            while True:
                new_field = deepcopy(self.field)
                intersection = False
                direction = choice([True, False])

                if direction:  # по горизонтали
                    random_coors = (randint(0, 10 - ship), randint(0, 9))
                    for x in range(random_coors[0], random_coors[0] + ship):
                        if x == random_coors[0]:
                            passed_cell = self.check_cell((x, random_coors[1]), True)
                        else:
                            passed_cell = self.check_cell((x, random_coors[1]), False)

                        if not passed_cell:
                            intersection = True
                            break
                        else:
                            new_field[random_coors[1]][x] = 1

                else:  # по вертикали
                    random_coors = (randint(0, 9), randint(0, 10 - ship))
                    for y in range(random_coors[1], random_coors[1] + ship):
                        if y == random_coors[1]:
                            passed_cell = self.check_cell((random_coors[0], y), True)
                        else:
                            passed_cell = self.check_cell((random_coors[0], y), False)

                        if not passed_cell:
                            intersection = True
                            break
                        else:
                            new_field[y][random_coors[0]] = 1
                # print(ship)
                # for i in new_field:
                # print(i)
                if not intersection:
                    self.field = deepcopy(new_field)
                    break

    def save_to_map_json(self):
        with open('map.json', 'w', encoding='utf8') as file:
            dump({"maps": self.field}, file)

from string import ascii_lowercase
from random import randint, choice
from copy import deepcopy

class Battle_ships:
    def __init__(self):
        self.alphabet = [i for i in 'aбвгдеёжзийклмнопкрстуфкцчшщъыьэюя']
        self.reversed_alphabet = {j: i for i, j in enumerate(self.alphabet)}
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

    def place_ships(self):
        ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for ship in ships:
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

        for i in self.field:
            print(i)

    def save_to_map_json(self):
        with open('maps.json', 'w', encoding='utf8') as file:
            file.write()


b = Battle_ships()
b.place_ships()

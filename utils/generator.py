import random


class Generator:
    def __init__(self, sudoku_type):
        if sudoku_type == 'sudoku4x4':
            self.__max_sudoku_number = 4
            self.__extra_rules = None
        elif sudoku_type == 'sudoku6x6':
            self.__max_sudoku_number = 6
            self.__extra_rules = None
        elif sudoku_type == 'sudoku9x9':
            self.__max_sudoku_number = 9
            self.__extra_rules = None
        elif sudoku_type == 'sudoku16x16':
            self.__max_sudoku_number = 16
            self.__extra_rules = None

        self.__board = [0 for x in range(self.__max_sudoku_number * self.__max_sudoku_number)]

    def rnd_num(self):
        return random.randrange(0, self.__max_sudoku_number) + 1


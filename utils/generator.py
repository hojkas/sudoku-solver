import random
from utils.strategy_manager import *


def rnd_num_from(options):
    return options[random.randrange(0, len(options))]


class Generator:
    def __init__(self, max_sudoku_number, sudoku_type_name, sector_ids=None):
        self.__max_sudoku_number = max_sudoku_number
        # acceptable types: "classic", "diagonal", "centers", "diagonal_centers", "hypersudoku", "jigsaw"
        self.__strategy_applier = StrategyApplier(max_sudoku_number, sudoku_type_name, False, sector_ids)

        if sudoku_type_name == 'something' and max_sudoku_number == 9:
            self.__cell_order = [0, 10, 20, 30, 40, 50, 60, 70, 80, 8, 16, 24, 32, 48, 56, 64, 72,
                                 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 17,
                                 18, 19, 21, 22, 23, 25, 26, 27, 28, 29, 31, 33, 34, 35,
                                 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 49, 51, 52, 53,
                                 54, 55, 57, 58, 59, 61, 62, 63, 65, 66, 67, 68, 69, 71,
                                 73, 74, 75, 76, 77, 78, 79]
        else:
            self.__cell_order = [x for x in range(max_sudoku_number*max_sudoku_number)]

    def generate(self, difficulty='true_random'):
        sudoku = SudokuBoard(self.__max_sudoku_number)
        if self.generate_next(sudoku, 0):
            return sudoku
        else:
            return None

    def generate_next(self, sudoku, cell_order_id):
        options = self.get_options()

        found_solution = False

        while len(options) != 0:
            num = rnd_num_from(options)
            options.remove(num)

            sudoku.cells[self.__cell_order[cell_order_id]].solved = num

            if self.has_mistakes(sudoku):
                continue

            if cell_order_id + 1 < (self.__max_sudoku_number * self.__max_sudoku_number):
                found_solution = self.generate_next(sudoku, cell_order_id + 1)
                if found_solution:
                    break
            else:
                # no next cell and no collisions == full board generated
                return True

        if not found_solution:
            # didn't find solution, remove this number
            sudoku.cells[self.__cell_order[cell_order_id]].solved = None

        return found_solution

    def is_solved(self, sudoku):
        return sudoku.is_fully_solved()

    def has_mistakes(self, sudoku):
        if self.__strategy_applier.has_obvious_mistakes(sudoku) is None:
            return False
        return True

    def rnd_num(self):
        return random.randrange(0, self.__max_sudoku_number) + 1

    def get_options(self):
        return [x + 1 for x in range(self.__max_sudoku_number)]

class SudokuBoard:
    def __init__(self, max_sudoku_number=9):
        self.max_sudoku_number = max_sudoku_number
        self.cells = []
        for i in range(max_sudoku_number * max_sudoku_number):
            self.cells.append(SudokuCell(i, max_sudoku_number))

    def fill_candidates_in_all_not_solved(self):
        for i in range(self.max_sudoku_number * self.max_sudoku_number):
            if not self.cells[i].is_solved():
                self.cells[i].fill_in_all_candidates()

    def is_fully_solved(self):
        for i in range(self.max_sudoku_number * self.max_sudoku_number):
            if not self.cells[i].is_solved():
                return False
        return True

    def has_unsolvable_cell(self):
        for i in range(self.max_sudoku_number * self.max_sudoku_number):
            if not self.cells[i].is_solved():
                if len(self.cells[i].notes) == 0:
                    return True
        return False

    # TODO only test function
    def print_full_sudoku(self):
        divider = '#-------#-------#-------#'
        for x in range(self.max_sudoku_number):
            if x % 3 == 0:
                print(divider)
            for y in range(self.max_sudoku_number):
                if y % 3 == 0:
                    print('| ', end='')
                self.cells[x * self.max_sudoku_number + y].print_solved_cell()
                print(' ', end='')
            print('|')
        print(divider)

    # tODO only test
    def print_full_4(self):
        divider = '#-----#-----#'
        for x in range(self.max_sudoku_number):
            if x % 2 == 0:
                print(divider)
            for y in range(self.max_sudoku_number):
                if y % 2 == 0:
                    print('| ', end='')
                self.cells[x * self.max_sudoku_number + y].print_solved_cell()
                print(' ', end='')
            print('|')
        print(divider)

    # TODO only test function
    def print_all_cells(self):
        for i in range(self.max_sudoku_number * self.max_sudoku_number):
            self.cells[i].print_full_cell()


class SudokuCell:
    def __init__(self, cell_id, max_sudoku_number=9):
        self.solved = None
        self.notes = []
        self.max_sudoku_number = 9
        self.cell_id = cell_id

    def fill_in_solved(self, num):
        self.solved = num
        self.notes = []

    def fill_in_note(self, num):
        if self.solved:
            self.add_to_notes(self.solved)
        self.solved = None
        self.add_to_notes(num)

    def add_to_notes(self, num):
        if num not in self.notes:
            self.notes.append(num)
            self.notes.sort()

    def is_solved(self):
        if self.solved is None:
            return False
        else:
            return True

    def fill_in_all_candidates(self):
        self.solved = None
        self.notes = []
        for i in range(1, self.max_sudoku_number + 1):
            self.notes.append(i)

    def count_candidates(self):
        return len(self.notes)

    # TODO only test function
    def print_full_cell(self):
        print('(', self.cell_id, ') ', end='', sep='')
        if self.solved:
            print(self.solved)
        else:
            print('--- [ ', end='')
            for val in self.notes:
                print(val, end=' ')
            print(']')

    # TODO only test function
    def print_solved_cell(self):
        if self.solved:
            print(self.solved, end='')
        else:
            print(' ', end='')

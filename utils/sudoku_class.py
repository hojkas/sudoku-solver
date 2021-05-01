class SudokuBoard:
    def __init__(self, max_sudoku_number=9):
        self.max_sudoku_number = max_sudoku_number
        self.cells = []
        for i in range(max_sudoku_number * max_sudoku_number):
            self.cells.append(SudokuCell(i, max_sudoku_number))

    def copy(self):
        new = SudokuBoard(self.max_sudoku_number)
        for i in range(self.max_sudoku_number * self.max_sudoku_number):
            new.cells[i] = self.cells[i].copy()
        return new

    def restore_notes_copy(self):
        new = SudokuBoard(self.max_sudoku_number)
        for i in range(self.max_sudoku_number * self.max_sudoku_number):
            if self.cells[i].solved is not None:
                new.cells[i] = self.cells[i].copy()
        return new

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

    def clear_cell(self, cell_id):
        self.cells[cell_id].notes = [x for x in range(1, self.max_sudoku_number+1)]
        self.cells[cell_id].solved = None

    def fill_cell(self, cell_id, number):
        self.cells[cell_id].notes = []
        self.cells[cell_id].solved = number

    # only test function
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

    # only test
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

    # only test function
    def print_all_cells(self):
        for i in range(self.max_sudoku_number * self.max_sudoku_number):
            self.cells[i].print_full_cell()


class SudokuCell:
    def __init__(self, cell_id, max_sudoku_number=9):
        self.solved = None
        self.notes = []
        self.max_sudoku_number = 9
        self.cell_id = cell_id

    def copy(self):
        new = SudokuCell(self.cell_id, self.max_sudoku_number)
        new.solved = self.solved
        new.notes = self.notes.copy()
        return new

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

    # only test function
    def print_full_cell(self):
        print('(', self.cell_id, ') ', end='', sep='')
        if self.solved:
            print(self.solved)
        else:
            print('--- [ ', end='')
            for val in self.notes:
                print(val, end=' ')
            print(']')

    # only test function
    def print_solved_cell(self):
        if self.solved:
            print(self.solved, end='')
        else:
            print(' ', end='')

from utils.sudoku_class import *
from utils.sudoku_convertor import *
from utils.strategy_manager import *

s = SudokuBoard(9)
s.fill_candidates_in_all_not_solved()
s.cells[0].fill_in_solved(1)
s.cells[1].fill_in_solved(2)
s.cells[2].notes = [1, 2, 3]
s.cells[3].notes = [1, 2, 3, 4]
s.cells[5].notes = [1, 2]
s.cells[6].notes = [1, 3]
l = collect_cell_candidates_info_list(s, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], limit=9)
res = naked_triple_check_for_groups(l)
print(res)

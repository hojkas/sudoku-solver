from utils.sudoku_class import *
from utils.sudoku_convertor import *
from utils.strategy_manager import *

s = SudokuBoard(9)
s.fill_candidates_in_all_not_solved()
s.cells[5].fill_in_solved(6)
s.cells[6].fill_in_solved(7)
s.cells[7].fill_in_solved(8)
s.cells[8].fill_in_solved(9)

s.cells[0].notes = [1, 2, 3, 4]
s.cells[1].notes = [1, 2, 3, 4]
s.cells[2].notes = [2, 3]
s.cells[3].notes = [2, 3, 4]
s.cells[4].notes = [8,9]
l = collect_candidate_occurences_info_list(s, [0, 1, 2, 3, 4, 5, 6, 7, 8], limit=4)
res = hidden_triple_check_for_groups(l)
# print(l)
print(res)

from utils.sudoku_class import *
from utils.sudoku_convertor import *
from utils.strategy_manager import *

sa = StrategyApplier(9, 'classic')
l = [0, 11]
print('Expected: sector')
print('Got: ', sa.get_ids_group_block_names(l))
l = [0, 1]
print('Expected: sector, row')
print('Got: ', sa.get_ids_group_block_names(l))
l = [10, 40]
print('Expected: nothing')
print('Got: ', sa.get_ids_group_block_names(l))
l = [10, 37]
print('Expected: col')
print('Got: ', sa.get_ids_group_block_names(l))
print('=========================')
sa = StrategyApplier(9, 'diagonal')
l = [0, 11]
print('Expected: sector')
print('Got: ', sa.get_ids_group_block_names(l))
l = [0, 1]
print('Expected: sector, row')
print('Got: ', sa.get_ids_group_block_names(l))
l = [10, 40]
print('Expected: diagonal_a')
print('Got: ', sa.get_ids_group_block_names(l))
l = [10, 37]
print('Expected: col')
print('Got: ', sa.get_ids_group_block_names(l))
print('========================')
sa = StrategyApplier(9, 'diagonal_centers')
l = [0, 11]
print('Expected: sector')
print('Got: ', sa.get_ids_group_block_names(l))
l = [0, 1]
print('Expected: sector, row')
print('Got: ', sa.get_ids_group_block_names(l))
l = [10, 40]
print('Expected: diagonal_a, center')
print('Got: ', sa.get_ids_group_block_names(l))
l = [10, 37]
print('Expected: col, center')
print('Got: ', sa.get_ids_group_block_names(l))

print('==========================')
print('FUN: ', sa.get_ids_group_block_names([40]))

"""
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
"""
from utils.sudoku_class import *
from utils.sudoku_convertor import *
from utils.strategy_manager import *

test_naked_single = [
    5, 3, None, None, 7, None, None, None, None,
    6, None, None, 1, 9, 5, None, None, None,
    None, 9, 8, None, None, None, None, 6, None,
    8, None, None, None, 6, None, None, None, 3,
    4, None, None, 8, None, 3, None, None, 1,
    7, None, None, None, 2, None, None, None, 6,
    None, 6, None, None, None, None, 2, 8, None,
    None, None, None, 4, 1, 9, None, None, 5,
    None, None, None, None, 8, None, None, 7, 9
]

test_hidden_single = [
    None, None, None, None, None, None, None, None, None,
    2, None, None, None, None, None, None, None, None,
    3, None, None, None, None, None, None, None, 2,
    None, 1, None, None, None, None, None, None, 3,
    None, None, None, None, None, None, None, None, 4,
    None, None, None, None, None, None, None, None, 5,
    None, None, 1, None, None, None, None, None, 6,
    None, None, None, None, None, None, None, None, 7,
    None, None, None, None, None, None, None, None, 8
]

test_json = {"max_sudoku_number": 9, "board": [{"cell_id": 0, "notes": [], "solved": 5}, {"cell_id": 1, "notes": [], "solved": 3}, {"cell_id": 2, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 3, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 4, "notes": [], "solved": 7}, {"cell_id": 5, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 6, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 7, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 8, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 9, "notes": [], "solved": 6}, {"cell_id": 10, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 11, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 12, "notes": [], "solved": 1}, {"cell_id": 13, "notes": [], "solved": 9}, {"cell_id": 14, "notes": [], "solved": 5}, {"cell_id": 15, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 16, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 17, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 18, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 19, "notes": [], "solved": 9}, {"cell_id": 20, "notes": [], "solved": 8}, {"cell_id": 21, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 22, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 23, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 24, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 25, "notes": [], "solved": 6}, {"cell_id": 26, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 27, "notes": [], "solved": 8}, {"cell_id": 28, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 29, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 30, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 31, "notes": [], "solved": 6}, {"cell_id": 32, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 33, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 34, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 35, "notes": [], "solved": 3}, {"cell_id": 36, "notes": [], "solved": 4}, {"cell_id": 37, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 38, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 39, "notes": [], "solved": 8}, {"cell_id": 40, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 41, "notes": [], "solved": 3}, {"cell_id": 42, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 43, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 44, "notes": [], "solved": 1}, {"cell_id": 45, "notes": [], "solved": 7}, {"cell_id": 46, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 47, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 48, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 49, "notes": [], "solved": 2}, {"cell_id": 50, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 51, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 52, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 53, "notes": [], "solved": 6}, {"cell_id": 54, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 55, "notes": [], "solved": 6}, {"cell_id": 56, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 57, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 58, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 59, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 60, "notes": [], "solved": 2}, {"cell_id": 61, "notes": [], "solved": 8}, {"cell_id": 62, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 63, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 64, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 65, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 66, "notes": [], "solved": 4}, {"cell_id": 67, "notes": [], "solved": 1}, {"cell_id": 68, "notes": [], "solved": 9}, {"cell_id": 69, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 70, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 71, "notes": [], "solved": 5}, {"cell_id": 72, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 73, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 74, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 75, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 76, "notes": [], "solved": 8}, {"cell_id": 77, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 78, "notes": [1, 2, 3, 4, 5, 6, 7, 8, 9], "solved": None}, {"cell_id": 79, "notes": [], "solved": 7}, {"cell_id": 80, "notes": [], "solved": 9}]}


# ============ CHANGE HERE ==============
# source_sudoku = test_hidden_single
# =======================================

# creation of board
# sudoku = convert_simple_array_to_sudoku_board(source_sudoku, 9)
sudoku = convert_js_json_to_sudoku_board(test_json)
sa = StrategyApplier(9, 'classic', collect_report=False)

# prep
# sa.fill_with_candidates(sudoku)
# sa.remove_all_collisions(sudoku)





exit(0)

print('SOLVING START\n==================\n')
i = 0
while True:
    # if sudoku is already solved, breaks
    if sudoku.is_fully_solved():
        break

    sudoku.print_full_sudoku()
    i += 1
    print(i, '. iteration', sep='')

    # fill in single candidates
    if sa.naked_single(sudoku):
        sa.remove_all_collisions(sudoku)
        continue

    if sa.hidden_single(sudoku):
        sa.remove_all_collisions(sudoku)
        continue

    # if none of the strategies is applicable, breaks
    break

sudoku.print_full_sudoku()
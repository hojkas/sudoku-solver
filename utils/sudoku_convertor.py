from utils.sudoku_class import *
# author: Iveta Strnadová (xstrna14)

""" sudoku_convertor.py serves as middle layer between simple array from generator.py
    and complex class from sudoku_class.py
"""


def convert_simple_array_to_sudoku_board(sudoku_array, max_sudoku_number):
    if len(sudoku_array) != (max_sudoku_number * max_sudoku_number):
        return None
    sboard = SudokuBoard(max_sudoku_number)
    for i, val in enumerate(sudoku_array):
        if val is not None:
            if 0 < val <= max_sudoku_number:
                sboard.cells[i].fill_in_solved(val)
    return sboard


def convert_js_json_to_sudoku_board(json):
    sboard = SudokuBoard(json['max_sudoku_number'])
    for cell in json['board']:
        if cell['solved'] is None:
            sboard.cells[cell['cell_id']].notes = cell['notes']
        else:
            sboard.cells[cell['cell_id']].solved = cell['solved']
    return sboard

def convert_sudoku_board_to_simple_array(sudoku_board):
    sarray = []
    for i in range(0, sudoku_board.max_sudoku_number * sudoku_board.max_sudoku_number):
        sarray.append(sudoku_board.cells[i].solved)
    return sarray

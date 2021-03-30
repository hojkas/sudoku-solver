from sudoku_class import *

""" sudoku_convertor.py serves as middle layer between simple array from generator.py
    and complex class from sudoku_class.py
"""

def convert_simple_array_to_sudoku_board(sudoku_array, max_sudoku_number):
    if len(sudoku_array) != (max_sudoku_number * max_sudoku_number):
        return None
    sboard = SudokuBoard(max_sudoku_number)
    for i, val in enumerate(sudoku_array):
        if val is not None:
            if val > 0 and val <= max_sudoku_number:
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
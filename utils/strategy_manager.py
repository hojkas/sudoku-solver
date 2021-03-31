from utils.sudoku_class import *
from django.utils.translation import gettext as _

""" Function fills non-solved cells with all possible candidate numbers
@param sudokou Current state of sudoku upon which the operation is executed.
"""


def fill_with_candidates(sudoku):
    sudoku.fill_candidates_in_all_not_solved()


class StrategyApplier:
    def __init__(self, max_sudoku_number, sudoku_type_name, collect_report=True):
        """ Inicialization of StrategyApplier creates number of variables derived from
        max_sudoku_number and sudoku_type_name that help to apply strategies more effectively
        without doing the same math operations repeatedly.
        @param max_sudoku_number Highest number in sudoku/number of possible options/number of columns
            and rows and such.
        @param sudoku_type_name Type of sudoku to derive extra rules. TODO only supports "classic" at the
            moment.
        """
        self.__max_sudoku_number = max_sudoku_number
        self.__cell_id_limit = max_sudoku_number * max_sudoku_number
        self.__row_ids = []
        self.__col_ids = []
        self.__sector_ids = []
        self.__extras_ids = []
        self.__cell_id_mapping = {}
        self.__collect_report = collect_report
        self.__report_json = {
            'strategy_applied': None,
            'text': None,
            'highlight': [],
            'candidates_to_remove': [],
            'success': None,
            'solve_number': None
        }

        for x in range(max_sudoku_number):
            c = []
            r = []
            for y in range(max_sudoku_number):
                r.append(x * max_sudoku_number + y)
                c.append(x + max_sudoku_number * y)
            self.__col_ids.append(c)
            self.__row_ids.append(r)

        if sudoku_type_name == "classic":
            if max_sudoku_number == 6:
                sectors_width = 3
                sectors_height = 2
            elif max_sudoku_number == 9:
                sectors_height = 3
                sectors_width = 3
            elif max_sudoku_number == 4:
                sectors_height = 2
                sectors_width = 2
            elif max_sudoku_number == 16:
                sectors_height = 4
                sectors_width = 4

            for i in range(sectors_height):
                for j in range(sectors_width):
                    starting_x = i * sectors_height
                    starting_y = j * sectors_width
                    s = []
                    for k in range(sectors_height):
                        for l in range(sectors_width):
                            s.append((starting_x + k) * max_sudoku_number + (starting_y + l))
                    self.__sector_ids.append(s)

        else:
            print('NOT SUPPORTED YET')
        # creating mapping for cells_id to row_ids, col_ids and sector_ids the cell is in
        # for quicker usage
        # creating empty dictionaries for each cell with key being its id
        for cell_id in range(max_sudoku_number * max_sudoku_number):
            self.__cell_id_mapping[cell_id] = {}
            # going through row "chunks" (list of list of ids in row, one chunk = one row) to register
        # the mapping
        for row_chunk_id, row_chunk in enumerate(self.__row_ids):
            for cell_id in row_chunk:
                self.__cell_id_mapping[cell_id]['row_id'] = row_chunk_id
        # the same for col and sector
        for col_chunk_id, col_chunk in enumerate(self.__col_ids):
            for cell_id in col_chunk:
                self.__cell_id_mapping[cell_id]['col_id'] = col_chunk_id
        for sector_chunk_id, sector_chunk in enumerate(self.__sector_ids):
            for cell_id in sector_chunk:
                self.__cell_id_mapping[cell_id]['sector_id'] = sector_chunk_id
        for extras_chunk_id, extras_chunk in enumerate(self.__extras_ids):
            for cell_id in extras_chunk:
                pass
                # figure out extras chunks mapping or don't and do it differently TODO

    # HELP functions for report collection
    def report_add_highlight(self, cell_id, is_solved, color, note_id=None):
        self.__report_json['highlight'].append({
            "cell_id": cell_id,
            "is_solved": is_solved,
            "note_id": note_id,
            "color": color
        })

    def report_add_candidate_to_remove(self, cell_id, note_id):
        self.__report_json['candidates_to_remove'].append({
            "cell_id": cell_id,
            "note_id": note_id
        })

    def report_add_solved_number(self, cell_id, number):
        pass

    # ENTRY POINT
    def find_next_step(self, sudoku):
        # check if sudoku is already solved
        if sudoku.is_fully_solved():
            self.__report_json['success'] = False
            self.__report_json['text'] = _('Sudoku už je vyřešené.')
            return self.__report_json

        # check if sudoku has truly empty cells, thus unsolvable
        if sudoku.has_unsolvable_cell():
            self.__report_json['success'] = False
            self.__report_json['text'] = _('Sudoku obsahuje alespoň jedno políčko, které není vyřešeno ani neobsahuje '
                                           'žádná možná kandidátní čísla. Takové sudoku není vyřešitelné. Pokud to '
                                           'není výsledek aplikací strategií programem, zkuste doplnit do prázdných '
                                           'políček všechny možné kandidáty a zkusit najít krok znovu.')
            return self.__report_json

        if self.remove_all_collisions(sudoku):
            return self.__report_json

        if self.naked_single(sudoku):
            return self.__report_json

        # TODO dát sem možná ještě check řešitelnosti a reflektovat to v odpovědi
        self.__report_json['text'] = _('Sudoku Helper nebyl schopen najít další logický krok. Toto může znamenat, '
                                       'že řešení neexistuje, nebo pouze že tento nástroj neumí tak složitou '
                                       'strategii, která by vedla k řešení.')
        self.__report_json['success'] = False
        return self.__report_json

    # REMOVE COLLISIONS
    """ Function removes any candidate number that is in the same row/column/sector as the
    same number that is already marked as solved.

    @param sudoku Current state of sudoku upon which the operation is executed.
    @returns bool True if function removed at least one candidate number
    """

    def remove_all_collisions(self, sudoku):
        changed_something = False

        for i in range(self.__cell_id_limit):
            if self.remove_collisions_around_cell(sudoku, i):
                changed_something = True

        if changed_something and self.__collect_report:
            self.__report_json['text'] = _('Nalezeny přímé kolize vyplněných čísel (žlutě) s možnými kandidáty '
                                           '(červeně).')
        return changed_something

    """ Function searches the row, col and sector (aka ids of other cells belonging to this
    block as defined upon StrategyApllier creation) and removes all candidate numbers
    in these cells with number equal to cell of which cell_id is given.

    @param sudoku Current state of sudoku upon which the operation is executed.
    @param cell_id Id of a cell with solved number that should be inspected in related row/col/sector.
    @returns bool True if any candidate number was eliminated in the process, false if not.
    """

    def remove_collisions_around_cell(self, sudoku, cell_id):
        changed_something = False
        row_id, col_id, sector_id = self.get_row_col_sector_id_of_cell(cell_id)
        # for row
        if sudoku.cells[cell_id].is_solved():
            num = sudoku.cells[cell_id].solved
            # for each other id in cells row block/col block/sector
            for cell_id_2 in (self.__row_ids[row_id]+self.__col_ids[col_id]+self.__sector_ids[sector_id]):
                # excluding the current one
                if cell_id == cell_id_2:
                    continue
                # if cell isn't already solved
                if not sudoku.cells[cell_id_2].is_solved():
                    # if the number is still in notes
                    if num in sudoku.cells[cell_id_2].notes:
                        if self.__collect_report:
                            self.__report_json['success'] = True
                            self.__report_json['strategy_applied'] = 'remove_collisions'
                            # color solved number that caused the collision elimination
                            self.report_add_highlight(cell_id, True, "yellow")
                            # color the canddiate to be eliminated
                            self.report_add_highlight(cell_id=cell_id_2, is_solved=False, color="red", note_id=num)
                            # mark the candidate for elimination
                            self.report_add_candidate_to_remove(cell_id_2, num)
                        else:
                            # it is removed (number solved in same block excludes its posibility)
                            sudoku.cells[cell_id_2].notes.remove(num)
                        changed_something = True

        # for extras (eg. diagonal)
        if len(self.__extras_ids) != 0:
            # TODO extra sectors
            pass
        return changed_something

    """ Function returns id of row/col/sector the cell is part of.

    @param cell_id Id of cell to get position of.
    @returns (row_id, column_id, sector_id) Tuple consisting of row id, column id and sector id.
    """

    def get_row_col_sector_id_of_cell(self, cell_id):
        return (self.__cell_id_mapping[cell_id]['row_id'],
                self.__cell_id_mapping[cell_id]['col_id'],
                self.__cell_id_mapping[cell_id]['sector_id'])

    # NAKED SINGLE
    def naked_single(self, sudoku):
        changed_something = False
        for i in range(self.__cell_id_limit):
            if sudoku.cells[i].count_candidates() == 1:
                if self.__collect_report:
                    row_id = self.__cell_id_mapping[i]['row_id'] + 1
                    col_id = self.__cell_id_mapping[i]['col_id'] + 1
                    self.__report_json['solve_number'] = {"cell_id": i, "number": sudoku.cells[i].notes[0]}
                    self.__report_json['success'] = True
                    self.__report_json['strategy_applied'] = "naked_single"
                    self.__report_json['text'] = _('V políčku r' + str(row_id) + 'c' + str(col_id) +
                                                   ' se nachází pouze jedno možné kandidátní číslo.')
                    self.__report_json['highlight'].append({
                        'cell_id': i,
                        'is_solved': False,
                        'note_id': sudoku.cells[i].notes[0],
                        'color': 'green'
                    })
                    return True
                else:
                    sudoku.cells[i].fill_in_solved(sudoku.cells[i].notes[0])
                changed_something = True
        return changed_something

    # HIDDEN SINGLE
    def hidden_single(self, sudoku):
        # for every block chunk, aka area of sudoku where 1-max_sudoku_number can be once, like row, col, sector
        for block_chunk in (self.__row_ids + self.__col_ids + self.__sector_ids):
            # check all candidates if some is present only once (assuming remove_collisions very called beforehand)
            res = self.__find_candidates_with_n_occurences(sudoku, block_chunk, 1)
            if len(res) > 0:
                # res containes tuples with number that is only once mentioned and cell_id where it is
                for number, cell_ids in res:
                    sudoku.cells[cell_ids[0]].fill_in_solved(number)
                    return True
        return False

    """ Function to help with hidden single/pair/triple/quadruple
    @param sudoku Current state of sudoku upon which the operation is executed.
    @param block_ids List of cell ids which belong to one block
    @param target_number Int value of how many candidate occurencies we search for.
    @returns result List of tuples with numbers and cells of their occurence in the correct count.
    """

    def __find_candidates_with_n_occurences(self, sudoku, block_ids, target_number):
        occurence = {}
        res = []
        for num in range(1, self.__max_sudoku_number + 1):
            occurence[num] = []
        for cell_id in block_ids:
            for candidate in sudoku.cells[cell_id].notes:
                occurence[candidate].append(cell_id)
        for num in range(1, self.__max_sudoku_number + 1):
            # in searching for 1/2 occurences, it requires exactly target_number of occurences
            # for searching for 3/4, important combinations may occur not only with three 
            # triple-occurences, but also with 3 3 2 and so on, so it also marks 2+ occurences for them
            if ((target_number <= 2 and len(occurence[num]) == target_number) or
                    (target_number > 2 and len(occurence[num]) <= target_number
                     and len(occurence[num]) > 1)):
                res.append((num, occurence[num]))
        return res

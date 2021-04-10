from utils.sudoku_class import *
from django.utils.translation import gettext as _

def fill_with_candidates(sudoku):
    """ Function fills non-solved cells with all possible candidate numbers
    @param sudoku Current state of sudoku upon which the operation is executed.
    """
    sudoku.fill_candidates_in_all_not_solved()

def is_group_of_same_numbers(lists):
    s = set()
    for l in lists:
        s = s.union(set(l))
    if len(s) <= len(lists):
        return s
    return None

def collect_cell_candidates_info_list(sudoku, block_ids, limit=None):
    res = []
    for cell_id in block_ids:
        if sudoku.cells[cell_id].is_solved():
            continue
        if limit is not None:
            if len(sudoku.cells[cell_id].notes) > limit:
                continue
        res.append({'cell_id': cell_id,
                    'total': len(sudoku.cells[cell_id].notes),
                    'notes': sudoku.cells[cell_id].notes})
    return res

def collect_candidate_occurences_info_list(sudoku, block_ids, limit=None):
    prep_d = {}
    for n in range(1, sudoku.max_sudoku_number+1):
        prep_d[n] = {
            "num": n,
            "cell_ids": [],
            "total": 0
        }
    for cell_id in block_ids:
        if sudoku.cells[cell_id].is_solved():
            continue
        for note in sudoku.cells[cell_id].notes:
            prep_d[note]["total"] += 1
            prep_d[note]["cell_ids"].append(cell_id)

    res = []
    for key, value in prep_d.items():
        if value['total'] == 0:
            continue
        if limit is None or value['total'] <= limit:
            res.append(value)
    return res

def naked_triple_check_for_groups(cells_info_list):
    res = []
    len_of_list = len(cells_info_list)
    if len_of_list < 2:
        return []  # there can be no triple/quad if there is only 2- unsolved left
    # searching for groups consisting of 3 cells of max 3 same candidates
    for x in range(0, len_of_list):
        for y in range(x+1, len_of_list):
            for z in range(y+1, len_of_list):
                group = is_group_of_same_numbers([cells_info_list[x]['notes'],
                                                  cells_info_list[y]['notes'],
                                                  cells_info_list[z]['notes']])
                if group is not None:
                    res.append({
                        'cell_ids': [cells_info_list[x]['cell_id'],
                                     cells_info_list[y]['cell_id'],
                                     cells_info_list[z]['cell_id']],
                        'notes': list(group)
                    })

    # searching for groups consisting of 4 cells of max 4 same candidates
    for x in range(0, len_of_list):
        for y in range(x+1, len_of_list):
            for z in range(y+1, len_of_list):
                for k in range(z+1, len_of_list):
                    group = is_group_of_same_numbers([cells_info_list[x]['notes'],
                                                      cells_info_list[y]['notes'],
                                                      cells_info_list[z]['notes'],
                                                      cells_info_list[k]['notes']])
                    if group is not None:
                        res.append({
                            'cell_ids': [cells_info_list[x]['cell_id'],
                                         cells_info_list[y]['cell_id'],
                                         cells_info_list[z]['cell_id'],
                                         cells_info_list[k]['cell_id']],
                            'notes': list(group)
                        })
    return res

def hidden_triple_check_for_groups(candidate_info_list):
    """Finds groups of 3/4 hidden numbers in given info list.
    @param candidate_info_list List created by function collect_candidate_occurences_info_list.
    @return List of dictionary for each group found in format {"cell_ids": [list of group cell ids],
    "notes": [list of numbers creating group]}"""
    res = []
    len_of_list = len(candidate_info_list)
    if len_of_list <= 2:
        return res  # can't find triple in list of two or less

    # searching numbers to find group of 3
    for x in range(0, len_of_list):
        for y in range(x+1, len_of_list):
            for z in range(y+1, len_of_list):
                # test if cell ids of these numbers form group of max 3
                group = is_group_of_same_numbers([
                    candidate_info_list[x]['cell_ids'],
                    candidate_info_list[y]['cell_ids'],
                    candidate_info_list[z]['cell_ids']
                ])
                if group is not None:
                    res.append({
                        'cell_ids': list(group),
                        'notes': [
                            candidate_info_list[x]['num'],
                            candidate_info_list[y]['num'],
                            candidate_info_list[z]['num']
                        ]
                    })

    # searching for group of 4
    for x in range(0, len_of_list):
        for y in range(x+1, len_of_list):
            for z in range(y+1, len_of_list):
                for k in range(z+1, len_of_list):
                    # test if cell ids of these numbers form group of max 4
                    group = is_group_of_same_numbers([
                        candidate_info_list[x]['cell_ids'],
                        candidate_info_list[y]['cell_ids'],
                        candidate_info_list[z]['cell_ids'],
                        candidate_info_list[k]['cell_ids']
                    ])
                    if group is not None:
                        res.append({
                            'cell_ids': list(group),
                            'notes': [
                                candidate_info_list[x]['num'],
                                candidate_info_list[y]['num'],
                                candidate_info_list[z]['num'],
                                candidate_info_list[k]['num']
                            ]
                        })
    return res

def get_bold_num_list(num_list):
    res = ""
    for num in num_list:
        if res != "":
            res += ', '
        res += '<b>' + str(num) + '</b>'
    return res

class StrategyApplier:
    def __init__(self, max_sudoku_number, sudoku_type_name, collect_report=True):
        """ Inicialization of StrategyApplier creates number of variables derived from
        max_sudoku_number and sudoku_type_name that help to apply strategies more effectively
        without doing the same math operations repeatedly.
        @param max_sudoku_number Highest number in sudoku/number of possible options/number of columns
            and rows and such.
        @param sudoku_type_name Type of sudoku to derive extra rule.
        """
        self.__max_sudoku_number = max_sudoku_number
        self.__cell_id_limit = max_sudoku_number * max_sudoku_number
        self.__row_ids = []
        self.__col_ids = []
        self.__sector_ids = []
        self.__diagonal_a_ids = []
        self.__diagonal_b_ids = []
        self.__center_ids = []

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

        if sudoku_type_name in ["classic", "diagonal", "centers", "diagonal_centers"]:
            if max_sudoku_number == 6:
                sectors_width = 2
                sectors_height = 3
            elif max_sudoku_number == 9:
                sectors_height = 3
                sectors_width = 3
            elif max_sudoku_number == 4:
                sectors_height = 2
                sectors_width = 2
            elif max_sudoku_number == 16:
                sectors_height = 4
                sectors_width = 4

            for i in range(sectors_width):
                for j in range(sectors_height):
                    starting_x = i * sectors_height
                    starting_y = j * sectors_width
                    s = []
                    for k in range(sectors_height):
                        for l in range(sectors_width):
                            s.append((starting_x + k) * max_sudoku_number + (starting_y + l))
                    self.__sector_ids.append(s)

        else:
            print('NOT SUPPORTED YET')

        # creating extra ids blocks for diagonal + centers
        if sudoku_type_name in ["centers", "diagonal_centers"]:
            s = []
            for x in [1, 4, 7]:
                for y in [1, 4, 7]:
                    s.append(x * 9 + y)
            self.__center_ids = s
        if sudoku_type_name in ["diagonal", "diagonal_centers"]:
            diagonal_a = []
            diagonal_b = []
            for x in range(0, 9):
                diagonal_a.append(x * 9 + x)
                diagonal_b.append(x * 9 + (8 - x))
            self.__diagonal_a_ids = diagonal_a
            self.__diagonal_b_ids = diagonal_b

        # creating mapping for cells_id to row_ids, col_ids and sector_ids the cell is in
        # for quicker usage
        # creating empty dictionaries for each cell with key being its id
        for cell_id in range(max_sudoku_number * max_sudoku_number):
            self.__cell_id_mapping[cell_id] = {
                "diagonal_a": False,
                "diagonal_b": False,
                "center": False
            }
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

        # adding diagonal ids for diagonal sudokus
        if sudoku_type_name in ["diagonal", "diagonal_centers"]:
            for diagonal_id in self.__diagonal_a_ids:
                self.__cell_id_mapping[diagonal_id]["diagonal_a"] = True
            for diagonal_id in self.__diagonal_b_ids:
                self.__cell_id_mapping[diagonal_id]["diagonal_b"] = True

        # adding flag they are centers for center sudokus cells
        if sudoku_type_name in ["centers", "diagonal_centers"]:
            for center_id in self.__center_ids:
                self.__cell_id_mapping[center_id]["center"] = True

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
        self.__report_json['solve_number'] = {
            "cell_id": cell_id,
            "number": number
        }

    def get_cell_pos_str(self, cell_id):
        res = 'r' + str(int(cell_id/self.__max_sudoku_number) + 1) + 'c' + str(cell_id % self.__max_sudoku_number + 1)
        return res

    def get_bold_cell_pos_str(self, cell_id):
        return '<b>' + self.get_cell_pos_str(cell_id) + '</b>'

    def get_multiple_bold_cell_pos_str(self, cell_ids):
        res = ""
        for cell_id in cell_ids:
            if res != "":
                res += ', '
            res += self.get_bold_cell_pos_str(cell_id)
        return res

    # HELP function for functions
    def __apply_for_each(self, sudoku, func_name, name_of_unit, **kwargs):
        if name_of_unit == 'block':
            if self.__apply_for_each(sudoku, func_name, 'row', **kwargs):
                return True
            if self.__apply_for_each(sudoku, func_name, 'col', **kwargs):
                return True
            if self.__apply_for_each(sudoku, func_name, 'sector', **kwargs):
                return True
            if self.__apply_for_each(sudoku, func_name, 'diagonal_a', **kwargs):
                return True
            if self.__apply_for_each(sudoku, func_name, 'diagonal_b', **kwargs):
                return True
            if self.__apply_for_each(sudoku, func_name, 'center', **kwargs):
                return True
        elif name_of_unit == 'row':
            for set_of_ids in self.__row_ids:
                if func_name(sudoku, set_of_ids, 'row', **kwargs):
                    return True
        elif name_of_unit == 'col':
            for set_of_ids in self.__col_ids:
                if func_name(sudoku, set_of_ids, 'col', **kwargs):
                    return True
        elif name_of_unit == 'sector':
            for set_of_ids in self.__sector_ids:
                if func_name(sudoku, set_of_ids, 'sector', **kwargs):
                    return True
        elif name_of_unit == 'diagonal_a':
            if func_name(sudoku, self.__diagonal_a_ids, 'diagonal_a', **kwargs):
                return True
        elif name_of_unit == 'diagonal_b':
            if func_name(sudoku, self.__diagonal_b_ids, 'diagonal_b', **kwargs):
                return True
        elif name_of_unit == 'center':
            if func_name(sudoku, self.__center_ids, 'center', **kwargs):
                return True
        return False

    def has_obvious_mistakes(self, sudoku):
        collisions = {}
        for cell_id in range(self.__cell_id_limit):
            row_id, col_id, sector_id = self.get_row_col_sector_id_of_cell(cell_id)
            # preparing extra id chunks from diagonals/centers cell is in
            extra_ids = []
            if self.__cell_id_mapping[cell_id]['diagonal_a']:
                extra_ids += self.__diagonal_a_ids
            if self.__cell_id_mapping[cell_id]['diagonal_b']:
                extra_ids += self.__diagonal_b_ids
            if self.__cell_id_mapping[cell_id]['center']:
                extra_ids += self.__center_ids
            # for row
            if sudoku.cells[cell_id].is_solved():
                # for each other id in cells row block/col block/sector
                for cell_id_2 in (self.__row_ids[row_id] + self.__col_ids[col_id] + self.__sector_ids[sector_id]
                 + extra_ids):
                    # excluding the current one
                    if cell_id == cell_id_2:
                        continue
                    # if cell already solved
                    if sudoku.cells[cell_id_2].is_solved():
                        if sudoku.cells[cell_id].solved == sudoku.cells[cell_id_2].solved:
                            collisions[self.get_cell_pos_str(cell_id)] = True
        if len(collisions) == 0:
            return None
        else:
            s = ""
            for key in collisions.keys():
                s += key + ', '
            return s[:-2]

    # ENTRY POINT
    def find_next_step(self, sudoku):
        # check if sudoku is already solved
        if sudoku.is_fully_solved():
            self.__report_json['success'] = False
            self.__report_json['text'] = _('Sudoku už je vyřešené.')
            return self.__report_json

        # check if sudoku isn't obviously wrong
        collisions = self.has_obvious_mistakes(sudoku)
        if collisions is not None:
            self.__report_json['success'] = False
            self.__report_json['text'] = _('V sudoku se nachází vyplněná číslice v přímé kolizi. '
                                           'Sudoku není vyřešitelné. Kolize na pozicích: ' + collisions)
            return self.__report_json

        # check if sudoku has truly empty cells, thus unsolvable
        if sudoku.has_unsolvable_cell():
            self.__report_json['success'] = False
            self.__report_json['text'] = _('Sudoku obsahuje alespoň jedno políčko, které není vyřešeno ani neobsahuje '
                                           'žádná možná kandidátní čísla. Takové sudoku není vyřešitelné. Pokud to '
                                           'není výsledek aplikací strategií programem, zkuste doplnit do prázdných '
                                           'políček všechna možná kandidátní čísla a zkusit najít krok znovu.')
            return self.__report_json

        if self.remove_all_collisions(sudoku):
            return self.__report_json

        if self.naked_single(sudoku):
            return self.__report_json

        if self.hidden_single(sudoku):
            return self.__report_json

        if self.naked_pair(sudoku):
            return self.__report_json

        if self.__max_sudoku_number == 4:
            # sudoku 4x4 doesn't benefit from more complex strategies, thus ending here
            self.__report_json['text'] = _('Sudoku Helper nebyl schopen najít další logický krok. Toto může znamenat, '
                                           'že řešení neexistuje, nebo pouze že tento nástroj neumí tak složitou '
                                           'strategii, která by vedla k řešení.')
            self.__report_json['success'] = False
            return self.__report_json

        if self.hidden_pair(sudoku):
            return self.__report_json

        if self.naked_triple(sudoku):
            return self.__report_json

        if self.hidden_triple(sudoku):
            return self.__report_json

        self.__report_json['text'] = _('Sudoku Helper nebyl schopen najít další logický krok. Toto může znamenat, '
                                       'že řešení neexistuje, nebo pouze že tento nástroj neumí tak složitou '
                                       'strategii, která by vedla k řešení.')
        self.__report_json['success'] = False
        return self.__report_json

    # REMOVE COLLISIONS - DONE
    def remove_all_collisions(self, sudoku):
        """ Function removes any candidate number that is in the same row/column/sector as the
        same number that is already marked as solved.

        @param sudoku Current state of sudoku upon which the operation is executed.
        @returns bool True if function removed at least one candidate number
        """
        changed_something = False

        for i in range(self.__cell_id_limit):
            if self.remove_collisions_around_cell(sudoku, i):
                changed_something = True

        if changed_something and self.__collect_report:
            self.__report_json['text'] = _('Nalezeny přímé kolize vyplněných čísel (žlutě) s možnými kandidátními čísly'
                                           ' (červeně).')
        return changed_something

    def remove_collisions_around_cell(self, sudoku, cell_id):
        """ Function searches the row, col and sector (aka ids of other cells belonging to this
        block as defined upon StrategyApllier creation) and removes all candidate numbers
        in these cells with number equal to cell of which cell_id is given.

        @param sudoku Current state of sudoku upon which the operation is executed.
        @param cell_id Id of a cell with solved number that should be inspected in related row/col/sector.
        @returns bool True if any candidate number was eliminated in the process, false if not.
        """
        changed_something = False
        row_id, col_id, sector_id = self.get_row_col_sector_id_of_cell(cell_id)
        # preparing extra id chunks from diagonals/centers cell is in
        extra_ids = []
        if self.__cell_id_mapping[cell_id]['diagonal_a']:
            extra_ids += self.__diagonal_a_ids
        if self.__cell_id_mapping[cell_id]['diagonal_b']:
            extra_ids += self.__diagonal_b_ids
        if self.__cell_id_mapping[cell_id]['center']:
            extra_ids += self.__center_ids

        # for row
        if sudoku.cells[cell_id].is_solved():
            num = sudoku.cells[cell_id].solved
            # for each other id in cells row block/col block/sector
            for cell_id_2 in (self.__row_ids[row_id]+self.__col_ids[col_id]+self.__sector_ids[sector_id]+extra_ids):
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

        return changed_something

    def get_row_col_sector_id_of_cell(self, cell_id):
        """ Function returns id of row/col/sector the cell is part of.

        @param cell_id Id of cell to get position of.
        @returns (row_id, column_id, sector_id) Tuple consisting of row id, column id and sector id.
        """
        return (self.__cell_id_mapping[cell_id]['row_id'],
                self.__cell_id_mapping[cell_id]['col_id'],
                self.__cell_id_mapping[cell_id]['sector_id'])

    # NAKED SINGLE - DONE
    def naked_single(self, sudoku):
        """ Function searches through all cells in sudoku. In each one, it test if there isn't only one possible
        candidate. If this condition is met, the sole candidate is marked for filling/filled into the cell as solved.

        @param sudoku SudokuBoard instance with current state of sudoku.
        @return bool True if the strategy was found and applied, False if not.
        """
        changed_something = False
        for i in range(self.__cell_id_limit):
            if sudoku.cells[i].count_candidates() == 1:
                if self.__collect_report:
                    self.report_add_solved_number(i, sudoku.cells[i].notes[0])

                    self.__report_json['success'] = True
                    self.__report_json['strategy_applied'] = "naked_single"
                    self.__report_json['text'] = _('V políčku ' + self.get_bold_cell_pos_str(i) +
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

    # HIDDEN SINGLE - DONE
    def hidden_single(self, sudoku):
        """ Function searches through all blocks (rows, cols, sectors, extras) in sudoku. In each one, it tries to
        find candidate with only one occurence accross block. If this condition is met, the sole candidate is marked
        for filling/filled into the cell as solved.

        @param sudoku SudokuBoard instance with current state of sudoku.
        @return bool True if the strategy was found and applied, False if not.
        """
        return self.__apply_for_each(sudoku, self.hidden_single_on_one_block, 'block')

    def hidden_single_on_one_block(self, sudoku, ids_chunk, location):
        res = collect_candidate_occurences_info_list(sudoku, ids_chunk, 1)
        if len(res) > 0:
            # res containes tuples with number that is only once mentioned and cell_id where it is
            for info_dict in res:
                cell_ids = info_dict['cell_ids']
                number = info_dict['num']
                if self.__collect_report:
                    self.report_add_highlight(cell_ids[0], False, "green", number)
                    self.report_add_solved_number(cell_ids[0], number)
                    self.__report_json['success'] = True
                    self.__report_json['strategy_applied'] = 'hidden_single'
                    location_map = {
                        'row': _('v řádku'),
                        'col': _('v sloupci'),
                        'sector': _('v sektoru'),
                        'diagonal_a': _('na diagonále'),
                        'diagonal_b': _('na diagonále'),
                        'center': _('v centrech čtverců')
                    }
                    self.__report_json['text'] = _('V buňce ' + self.get_bold_cell_pos_str(cell_ids[0]) +
                           ' bude doplněno zeleně zvýrazněné kandidátní číslo, protože je to jediné možné '
                           'umístění číslice ' + location_map[location] + '.')
                else:
                    sudoku.cells[cell_ids[0]].fill_in_solved(number)
                return True
        return False

    # NAKED PAIR - DONE
    def naked_pair(self, sudoku):
        return self.__apply_for_each(sudoku, self.naked_pair_on_one_block, 'block')

    def naked_pair_on_one_block(self, sudoku, ids_chunk, location):
        cells_info_list = collect_cell_candidates_info_list(sudoku, ids_chunk)
        x = 0
        while x < len(cells_info_list):
            y = x + 1
            while y < len(cells_info_list):
                # compares each two cells if they have the same notes
                if cells_info_list[x]['total'] == 2 and cells_info_list[y]['total'] == 2:
                    if cells_info_list[x]['notes'] == cells_info_list[y]['notes']:
                        # found naked pair, but it is yet not determined if the naked pair makes any change
                        np_cell_id_1 = cells_info_list[x]['cell_id']
                        np_cell_id_2 = cells_info_list[y]['cell_id']
                        num_1, num_2 = cells_info_list[x]['notes']
                        something_changed = False
                        for cell_id in ids_chunk:
                            if cell_id == np_cell_id_1 or cell_id == np_cell_id_2:
                                continue
                            if num_1 in sudoku.cells[cell_id].notes:
                                # strategy naked pair can be applied to eliminate this candidate
                                self.apply_naked_pair_on_cell(sudoku, cell_id, num_1)
                                something_changed = True
                            if num_2 in sudoku.cells[cell_id].notes:
                                # strategy naked pair can be applied to eliminate this candidata
                                self.apply_naked_pair_on_cell(sudoku, cell_id, num_2)
                                something_changed = True
                        # if something changed == strategy can be applied to make a change
                        if something_changed:
                            if self.__collect_report:
                                self.report_add_highlight(np_cell_id_1, False, 'yellow', note_id=num_1)
                                self.report_add_highlight(np_cell_id_1, False, 'yellow', note_id=num_2)
                                self.report_add_highlight(np_cell_id_2, False, 'yellow', note_id=num_1)
                                self.report_add_highlight(np_cell_id_2, False, 'yellow', note_id=num_2)
                                self.__report_json['success'] = True
                                self.__report_json['strategy_applied'] = 'naked_pair'
                                location_mapper = {
                                    'col': _('tohoto sloupce'),
                                    'row': _('tohoto řádku'),
                                    'sector': _('tohoto sektoru'),
                                    'diagonal_a': _('této diagonály'),
                                    'diagonal_b': _('této diagonály'),
                                    'center': _('středů čtverců')
                                }
                                t = _('Buňky ' + self.get_bold_cell_pos_str(np_cell_id_1) + ' a ' +
                                      self.get_bold_cell_pos_str(np_cell_id_2) + ' obsahují pouze kandidátní čísla <b>'
                                      + str(num_1) + ',' + str(num_2) + '</b> (žlutě). Tato kandidátní čísla proto '
                                                                        'nemůžou být '
                                      + ' v ostatních buňkách ' + location_mapper[location] +
                                      ' (červeně).')
                                self.__report_json['text'] = t
                            return True
                y += 1
            x += 1
        return False

    def apply_naked_pair_on_cell(self, sudoku, cell_id, num):
        """Depending on variable __collect_report, either highlights candidate in cell with value num and marks
        it for removal, or removes it on spot."""
        if self.__collect_report:
            self.report_add_highlight(cell_id, False, 'red', note_id=num)
            self.report_add_candidate_to_remove(cell_id, num)
        else:
            sudoku.cells[cell_id].notes.remove(num)

    # HIDDEN PAIR - DONE
    def hidden_pair(self, sudoku):
        return self.__apply_for_each(sudoku, self.hidden_pair_on_one_block, 'block')

    def hidden_pair_on_one_block(self, sudoku, ids_chunk, location):
        info_list = collect_candidate_occurences_info_list(sudoku, ids_chunk, limit=2)
        info_list_len = len(info_list)
        for x in range(0, info_list_len):
            for y in range(x+1, info_list_len):
                # for each two candidates in block with only two occurences
                if info_list[x]['cell_ids'] == info_list[y]['cell_ids'] and len(info_list[x]['cell_ids']) == 2:
                    # found hidden pair, but it may not make change
                    num_1 = info_list[x]['num']
                    num_2 = info_list[y]['num']
                    changed_something = False
                    for cell_id in info_list[x]['cell_ids']:
                        for n in range(1, self.__max_sudoku_number + 1):
                            if n == num_1 or n == num_2:
                                continue
                            if n in sudoku.cells[cell_id].notes:
                                # cell of hidden pair has other candidate that can be eliminated
                                changed_something = True
                                if self.__collect_report:
                                    self.report_add_highlight(cell_id, False, 'red', n)
                                    self.report_add_candidate_to_remove(cell_id, n)
                                else:
                                    sudoku.cells[cell_id].notes.remove(n)
                    # if something was changed, this pair was the hidden pair we looked for and strategy is complete
                    if changed_something:
                        # report collection
                        if self.__collect_report:
                            cell_id_1, cell_id_2 = info_list[x]['cell_ids']
                            self.report_add_highlight(cell_id_1, False, 'yellow', num_1)
                            self.report_add_highlight(cell_id_1, False, 'yellow', num_2)
                            self.report_add_highlight(cell_id_2, False, 'yellow', num_1)
                            self.report_add_highlight(cell_id_2, False, 'yellow', num_2)

                            self.__report_json['success'] = True
                            self.__report_json['strategy_applied'] = 'hidden_pair'
                            ids_str = self.get_multiple_bold_cell_pos_str(info_list[x]['cell_ids'])
                            num_str = get_bold_num_list([num_1, num_2])
                            location_mapper = {'row': _('v daném řádku'),
                                               'col': _('v daném sloupci'),
                                               'sector': _('v daném sektoru'),
                                               'diagonal_a': _('na dané diagonále'),
                                               'diagonal_b': _('na dané diagonále'),
                                               'center': _('mezi středy čtverců')
                                               }
                            self.__report_json['text'] = _('Buňky ' + ids_str + ' obsahují jako jediné ' +
                                    location_mapper[location] + ' kandidátní čísla ' + num_str + '(žlutě). Proto je v '
                                    'těchto buňkách možné odstranit všechna ostatní kandidátní čísla (červeně).')
                        return True
        return False

    # NAKED TRIPLE/QUAD - DONE
    def naked_triple(self, sudoku):
        return self.__apply_for_each(sudoku, self.naked_triple_on_one_block, 'block')

    def naked_triple_on_one_block(self, sudoku, ids_chunk, location):
        cells_info_list = collect_cell_candidates_info_list(sudoku, ids_chunk, limit=4)
        found_groups = naked_triple_check_for_groups(cells_info_list)
        if len(found_groups) != 0:
            # one or multiple groups were found, need to be checked if they have any effect
            for group in found_groups:
                changed_something = False
                for cell_id in ids_chunk:
                    if cell_id in group['cell_ids']:
                        continue
                    if sudoku.cells[cell_id].is_solved():
                        continue
                    # for each cell that is in this ids_chunk but is not part of group nor solved
                    # check if something actually changes by applying the strategy
                    for num in group['notes']:
                        # compares number found in group with cell candidates
                        if num in sudoku.cells[cell_id].notes:
                            changed_something = True
                            if self.__collect_report:
                                self.report_add_highlight(cell_id, False, 'red', note_id=num)
                                self.report_add_candidate_to_remove(cell_id, num)
                            else:
                                sudoku.cells[cell_id].notes.remove(num)
                # at this point, all possibilities of canddiate removal caused by this group have been check
                if changed_something:
                    if self.__collect_report:
                        # finishing report on this strategy
                        self.__report_json['success'] = True
                        self.__report_json['strategy_applied'] = 'naked_triple'
                        cell_pos_str = self.get_multiple_bold_cell_pos_str(group['cell_ids'])
                        num_list_str = get_bold_num_list(group['notes'])
                        for cell_id in group['cell_ids']:
                            for num in group['notes']:
                                if num in sudoku.cells[cell_id].notes:
                                    # num that is part of significant group in cell that is part of it is present
                                    # and should be highlighted
                                    self.report_add_highlight(cell_id, False, 'yellow', note_id=num)
                        location_mapper = {
                            'col': _('v jednom sloupci'),
                            'row': _('v jednom řádku'),
                            'sector': _('v jednom sektoru'),
                            'diagonal_a': _('na jedné diagonále'),
                            'diagonal_b': _('na jedné diagonále'),
                            'center': _('ve středech čtverců')
                        }
                        self.__report_json['text'] = _('V buňkách ' + cell_pos_str + ' se nachází pouze ' +
                                                       str(len(group['notes'])) + ' stejná kandidátní čísla ' +
                                                       num_list_str + ' (žlutě). Protože leží všechny tyto buňky '
                                                       + location_mapper[location] + ', je možno tato ' +
                                                       'kandidátní čísla z ostatních buňek bloku odstranit (červeně).')
                    return True
        return False

    # HIDDEN TRIPLE/QUAD
    def hidden_triple(self, sudoku):
        return self.__apply_for_each(sudoku, self.hidden_triple_on_one_block, 'block')

    def hidden_triple_on_one_block(self, sudoku, ids_chunk, location):
        info_list = collect_candidate_occurences_info_list(sudoku, ids_chunk, limit=4)
        found_groups = hidden_triple_check_for_groups(info_list)
        for group_d in found_groups:
            # have found hidden group of 3/4, now has to check if the group makes any change
            changed_something = False
            for cell_id in group_d['cell_ids']:
                notes = group_d['notes']
                for n in range(1, self.__max_sudoku_number + 1):
                    if n in notes:
                        continue
                    if n in sudoku.cells[cell_id].notes:
                        # in one of cells of found group, there is another candidate not part of group that
                        # can be erased
                        changed_something = True
                        if self.__collect_report:
                            self.report_add_highlight(cell_id, False, 'red', n)
                            self.report_add_candidate_to_remove(cell_id, n)
                        else:
                            sudoku.cells[cell_id].notes.remove(n)
            # end of search for one group
            if changed_something:
                if self.__collect_report:
                    self.__report_json['success'] = True
                    self.__report_json['strategy_applied'] = 'hidden_triple'
                    for cell_id in group_d['cell_ids']:
                        for n in group_d['notes']:
                            if n in sudoku.cells[cell_id].notes:
                                self.report_add_highlight(cell_id, False, 'yellow', n)
                    ids_str = self.get_multiple_bold_cell_pos_str(group_d['cell_ids'])
                    num_str = get_bold_num_list(group_d['notes'])
                    location_mapper = {'row': _('v daném řádku'),
                                       'col': _('v daném sloupci'),
                                       'sector': _('v daném sektoru'),
                                       'diagonal_a': _('na dané diagonále'),
                                       'diagonal_b': _('na dané diagonále'),
                                       'center': _('ve středech čtverců')
                    }
                    self.__report_json['text'] = _('Buňky ' + ids_str + ' obsahují jako jediné ' +
                                    location_mapper[location] + ' kandidátní čísla ' + num_str + ' (žlutě). Proto je v'
                                    ' těchto buňkách možné odstranit všechna ostatní kandidátní čísla (červeně).')
                return True
        return False



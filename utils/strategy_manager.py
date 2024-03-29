from utils.sudoku_class import *
from django.utils.translation import gettext as _
import copy

# author: Iveta Strnadová (xstrna14)

def fill_with_candidates(sudoku):
    """ Function fills non-solved cells with all possible candidate numbers
    @param sudoku Current state of sudoku upon which the operation is executed.
    """
    sudoku.fill_candidates_in_all_not_solved()


def is_group_of_same_numbers(lists):
    s = set()
    for l in lists:
        if not l:
            return None
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
    """ Function collects information about candidate placement in block_ids and returns dictionary with them.
    d = { "num": n --- numeric value of candidate
          "cell_ids": [X1, X2] --- list of cell_ids where candidate is
          "total": N --- total canddiate occurences
        }

    @param sudoku Sudoku board to search.
    @param block_ids Ids of cells forming block to be searched.
    @param limit If set, only candidates with total <= limit are returned
    @return Dictionary with information about candidate occurences.
    """
    prep_d = {}
    for n in range(1, sudoku.max_sudoku_number + 1):
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


def naked_triple_check_for_groups(cells_info_list, is_hexa_sudoku=False):
    res = []
    len_of_list = len(cells_info_list)
    if len_of_list < 2:
        return []  # there can be no triple/quad if there is only 2- unsolved left
    # searching for groups consisting of 3 cells of max 3 same candidates
    for x in range(0, len_of_list):
        for y in range(x + 1, len_of_list):
            for z in range(y + 1, len_of_list):
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
        for y in range(x + 1, len_of_list):
            for z in range(y + 1, len_of_list):
                for k in range(z + 1, len_of_list):
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

    # searching for 5-8 for 16x16 sudoku
    if is_hexa_sudoku:
        for n1 in range(0, len_of_list):
            for n2 in range(n1 + 1, len_of_list):
                for n3 in range(n2 + 1, len_of_list):
                    for n4 in range(n3 + 1, len_of_list):
                        for n5 in range(n4 + 1, len_of_list):
                            # check for five group
                            nums = [cells_info_list[i]['notes'] for i in [n1, n2, n3, n4, n5]]
                            group = is_group_of_same_numbers(nums)
                            if group is not None:
                                cell_ids = [cells_info_list[i]['cell_id'] for i in [n1, n2, n3, n4, n5]]
                                res.append({
                                    'cell_ids': cell_ids,
                                    'notes': list(group)
                                })
                            # continue with 6th item
                            for n6 in range(n5 + 1, len_of_list):
                                # check for six group
                                nums = [cells_info_list[i]['notes'] for i in [n1, n2, n3, n4, n5, n6]]
                                group = is_group_of_same_numbers(nums)
                                if group is not None:
                                    cell_ids = [cells_info_list[i]['cell_id'] for i in [n1, n2, n3, n4, n5, n6]]
                                    res.append({
                                        'cell_ids': cell_ids,
                                        'notes': list(group)
                                    })
                                # continue with 7th item
                                for n7 in range(n6 + 1, len_of_list):
                                    # check for seven group
                                    nums = [cells_info_list[i]['notes'] for i in [n1, n2, n3, n4, n5, n6, n7]]
                                    group = is_group_of_same_numbers(nums)
                                    if group is not None:
                                        cell_ids = [cells_info_list[i]['cell_id'] for i in [n1, n2, n3, n4, n5, n6, n7]]
                                        res.append({
                                            'cell_ids': cell_ids,
                                            'notes': list(group)
                                        })
                                    # continue with 8th item
                                    for n8 in range(n7 + 1, len_of_list):
                                        # check for eight group
                                        nums = [cells_info_list[i]['notes'] for i in [n1, n2, n3, n4, n5, n6, n7, n8]]
                                        group = is_group_of_same_numbers(nums)
                                        if group is not None:
                                            cell_ids = [cells_info_list[i]['cell_id']
                                                        for i in [n1, n2, n3, n4, n5, n6, n7, n8]]
                                            res.append({
                                                'cell_ids': cell_ids,
                                                'notes': list(group)
                                            })

    return res


def hidden_triple_check_for_groups(candidate_info_list, is_hexa_sudoku=False):
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
        for y in range(x + 1, len_of_list):
            for z in range(y + 1, len_of_list):
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
        for y in range(x + 1, len_of_list):
            for z in range(y + 1, len_of_list):
                for k in range(z + 1, len_of_list):
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

    # searching for 5-8 for 16x16 sudoku
    if is_hexa_sudoku:
        for n1 in range(0, len_of_list):
            for n2 in range(n1 + 1, len_of_list):
                for n3 in range(n2 + 1, len_of_list):
                    for n4 in range(n3 + 1, len_of_list):
                        for n5 in range(n4 + 1, len_of_list):
                            # check for five group
                            cell_ids = [candidate_info_list[i]['cell_ids'] for i in [n1, n2, n3, n4, n5]]
                            group = is_group_of_same_numbers(cell_ids)
                            if group is not None:
                                nums = [candidate_info_list[i]['num'] for i in [n1, n2, n3, n4, n5]]
                                res.append({
                                    'cell_ids': list(group),
                                    'notes': nums
                                })
                            # continue with 6th item
                            for n6 in range(n5 + 1, len_of_list):
                                # check for six group
                                cell_ids = [candidate_info_list[i]['cell_ids'] for i in [n1, n2, n3, n4, n5, n6]]
                                group = is_group_of_same_numbers(cell_ids)
                                if group is not None:
                                    nums = [candidate_info_list[i]['num'] for i in [n1, n2, n3, n4, n5, n6]]
                                    res.append({
                                        'cell_ids': list(group),
                                        'notes': nums
                                    })
                                # continue with 7th item
                                for n7 in range(n6 + 1, len_of_list):
                                    # check for seven group
                                    cell_ids = [candidate_info_list[i]['cell_ids'] for i in
                                                [n1, n2, n3, n4, n5, n6, n7]]
                                    group = is_group_of_same_numbers(cell_ids)
                                    if group is not None:
                                        nums = [candidate_info_list[i]['num'] for i in
                                                [n1, n2, n3, n4, n5, n6, n7]]
                                        res.append({
                                            'cell_ids': list(group),
                                            'notes': nums
                                        })

    return res


def get_bold_num_list(num_list):
    res = ""
    for num in num_list:
        if res != "":
            res += ', '
        res += '<b>' + str(num) + '</b>'
    return res


def select_the_other_note_on_two_note_cell(sudoku, cell_id, note):
    if note == sudoku.cells[cell_id].notes[0]:
        return sudoku.cells[cell_id].notes[1]
    return sudoku.cells[cell_id].notes[0]


class StrategyApplier:
    def __init__(self, max_sudoku_number, sudoku_type_name, collect_report=True, sector_ids=None):
        """ Inicialization of StrategyApplier creates number of variables derived from
        max_sudoku_number and sudoku_type_name that help to apply strategies more effectively
        without doing the same math operations repeatedly.
        @param max_sudoku_number Highest number in sudoku/number of possible options/number of columns
            and rows and such.
        @param sudoku_type_name Type of sudoku to derive extra rule.
        """
        self.__cycles = 0
        self.__sudoku_type_name = sudoku_type_name
        self.__max_sudoku_number = max_sudoku_number
        self.__cell_id_limit = max_sudoku_number * max_sudoku_number
        self.__row_ids = []
        self.__col_ids = []
        self.__sector_ids = []
        self.__diagonal_a_ids = []
        self.__diagonal_b_ids = []
        self.__center_ids = []
        self.__hyper_ids = [[], [], [], []]
        self.__dont_solve = False

        self.__strategy_difficulty_order = {
            'remove_collisions': 0,
            'naked_single': 1,
            'hidden_single': 2,
            'naked_pair': 3,
            'hidden_pair': 4,
            'naked_triple': 5,
            'hidden_triple': 6,
            'intersection_removal': 7,
            'x-wing': 8,
            'y-wing': 9,
            'swordfish': 10,
            'xy-chain': 11
        }
        self.__hardest_strategy = None

        self.__cell_id_mapping = {}
        self.__collect_report = collect_report
        self.__report_json = {
            'strategy_applied': None,
            'text': None,
            'highlight': [],
            'candidates_to_remove': [],
            'success': None,
            'solve_number': None,
            'chains': []
        }

        for x in range(max_sudoku_number):
            c = []
            r = []
            for y in range(max_sudoku_number):
                r.append(x * max_sudoku_number + y)
                c.append(x + max_sudoku_number * y)
            self.__col_ids.append(c)
            self.__row_ids.append(r)

        if sudoku_type_name in ["classic", "diagonal", "centers", "diagonal_centers", "hypersudoku"]:
            # creating sector ids for mentioned types
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
        elif sudoku_type_name == "jigsaw" and sector_ids is not None:
            self.__sector_ids = sector_ids
        else:
            # for not supported sudoku name
            self.__report_json['success'] = False
            self.__report_json['text'] = _('Tento typ sudoku nemá podporované hledání strategií.')
            self.__dont_solve = True
            return

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

        # creating hypersudoku centers
        if sudoku_type_name == "hypersudoku":
            self.__hyper_ids = [
                [10, 11, 12, 19, 20, 21, 28, 29, 30],
                [14, 15, 16, 23, 24, 25, 32, 33, 34],
                [46, 47, 48, 55, 56, 57, 64, 65, 66],
                [50, 51, 52, 59, 60, 61, 68, 69, 70]
            ]

        # creating mapping for cells_id to row_ids, col_ids and sector_ids the cell is in
        # for quicker usage
        # creating empty dictionaries for each cell with key being its id
        for cell_id in range(max_sudoku_number * max_sudoku_number):
            self.__cell_id_mapping[cell_id] = {
                "diagonal_a": False,
                "diagonal_b": False,
                "center": False,
                "hypersudoku": [False, False, False, False]
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

        # adding flag for hypersudoku cells
        if sudoku_type_name == "hypersudoku":
            for i in range(4):
                for cell_id in self.__hyper_ids[i]:
                    self.__cell_id_mapping[cell_id]["hypersudoku"][i] = True

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

    def report_add_chain(self, from_cell, from_note, to_cell, to_note):
        self.__report_json['chains'].append({
            'from_cell': from_cell,
            'from_note': from_note,
            'to_cell': to_cell,
            'to_note': to_note
        })

    def get_cell_pos_str(self, cell_id):
        res = 'r' + str(int(cell_id / self.__max_sudoku_number) + 1) + 'c' + str(cell_id % self.__max_sudoku_number + 1)
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

    def get_hardest_strategy_applied(self):
        return self.__hardest_strategy

    def add_strategy_applied(self, strategy_name):
        if self.__hardest_strategy is None:
            self.__hardest_strategy = strategy_name
        elif self.__strategy_difficulty_order[strategy_name] > self.__strategy_difficulty_order[
            self.__hardest_strategy]:
            self.__hardest_strategy = strategy_name

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
            if self.__apply_for_each(sudoku, func_name, 'hypersudoku', **kwargs):
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
        elif name_of_unit == 'hypersudoku':
            for set_of_ids in self.__hyper_ids:
                if func_name(sudoku, set_of_ids, 'hypersudoku', **kwargs):
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
            for i in range(4):
                if self.__cell_id_mapping[cell_id]['hypersudoku'][i]:
                    extra_ids += self.__hyper_ids[i]
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

    def get_ids_group_block_names(self, ids_list):
        blocks = []
        # are they all in one row?
        row = -1
        for cell_id in ids_list:
            if row == -1:
                row = int(cell_id / self.__max_sudoku_number)
            else:
                if row != int(cell_id / self.__max_sudoku_number):
                    row = -2
                    break
        if row >= 0:
            blocks.append('row')
        # are they all in one column?
        col = -1
        for cell_id in ids_list:
            if col == -1:
                col = cell_id % self.__max_sudoku_number
            else:
                if col != (cell_id % self.__max_sudoku_number):
                    col = -2
                    break
        if col >= 0:
            blocks.append('col')
        # are they in the same sector?
        for one_sector_ids in self.__sector_ids:
            in_same = True
            for cell_id in ids_list:
                if cell_id not in one_sector_ids:
                    in_same = False
                    break
            if in_same:
                blocks.append('sector')
                break
        # are they in diagonal?
        in_same = True
        for cell_id in ids_list:
            if cell_id not in self.__diagonal_a_ids:
                in_same = False
                break
        if in_same:
            blocks.append('diagonal_a')
        in_same = True
        for cell_id in ids_list:
            if cell_id not in self.__diagonal_b_ids:
                in_same = False
                break
        if in_same:
            blocks.append('diagonal_b')
        # are they in centers?
        in_same = True
        for cell_id in ids_list:
            if cell_id not in self.__center_ids:
                in_same = False
                break
        if in_same:
            blocks.append('center')
        # are they in same hypersudoku sector?
        for i in range(4):
            in_same = True
            for cell_id in ids_list:
                if cell_id not in self.__hyper_ids[i]:
                    in_same = False
                    break
            if in_same:
                blocks.append('hypersudoku')
                break

        return blocks

    def cells_in_same_block(self, cell_id1, cell_id2):
        # cols?
        if (cell_id1 % self.__max_sudoku_number) == (cell_id2 % self.__max_sudoku_number):
            return True
        # rows?
        if int(cell_id1 / self.__max_sudoku_number) == int(cell_id2 / self.__max_sudoku_number):
            return True
        # sectors?
        for one_sector_ids in self.__sector_ids:
            if cell_id1 in one_sector_ids and cell_id2 in one_sector_ids:
                return True
        # diagonals?
        if cell_id1 in self.__diagonal_a_ids and cell_id2 in self.__diagonal_a_ids:
            return True
        if cell_id1 in self.__diagonal_b_ids and cell_id2 in self.__diagonal_b_ids:
            return True
        # centers?
        if cell_id1 in self.__center_ids and cell_id2 in self.__center_ids:
            return True
        # hypersudoku?
        for i in range(4):
            if cell_id1 in self.__hyper_ids[i] and cell_id2 in self.__hyper_ids[i]:
                return True
        # they are not
        return False

    # ENTRY POINT
    def find_next_step(self, sudoku):
        # if not supported, return immediately
        if self.__dont_solve:
            return self.__report_json

        # check if sudoku isn't obviously wrong
        collisions = self.has_obvious_mistakes(sudoku)
        if collisions is not None:
            if self.__collect_report:
                self.__report_json['success'] = False
                self.__report_json['text'] = _('V sudoku se nachází vyplněná číslice v přímé kolizi. '
                                               'Sudoku není vyřešitelné. Kolize na pozicích: ' + collisions)
                return self.__report_json
            else:
                return False

        # check if sudoku is already solved
        if sudoku.is_fully_solved():
            if self.__collect_report:
                self.__report_json['success'] = False
                self.__report_json['text'] = _('Sudoku už je vyřešené.')
                return self.__report_json
            else:
                return False

        # check if sudoku has truly empty cells, thus unsolvable
        if sudoku.has_unsolvable_cell():
            if self.__collect_report:
                self.__report_json['success'] = False
                self.__report_json['text'] = _(
                    'Sudoku obsahuje alespoň jedno políčko, které není vyřešeno ani neobsahuje '
                    'žádná možná kandidátní čísla. Takové sudoku není vyřešitelné. Pokud to '
                    'není výsledek aplikací strategií programem, zkuste doplnit do prázdných '
                    'políček všechna možná kandidátní čísla a zkusit najít krok znovu.')
                return self.__report_json
            else:
                return False

        if self.remove_all_collisions(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('remove_collisions')
                return True

        if self.naked_single(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('naked_single')
                return True

        if self.hidden_single(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('hidden_single')
                return True

        if self.naked_pair(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('naked_pair')
                return True

        if self.__max_sudoku_number == 4:
            if self.__collect_report:
                # sudoku 4x4 doesn't benefit from more complex strategies, thus ending here
                self.__report_json['text'] = _(
                    'Sudoku Helper nebyl schopen najít další logický krok. Toto může znamenat, '
                    'že řešení neexistuje, nebo pouze že tento nástroj neumí tak složitou '
                    'strategii, která by vedla k řešení.')
                self.__report_json['success'] = False
                return self.__report_json
            else:
                return False

        if self.hidden_pair(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('hidden_pair')
                return True

        if self.naked_triple(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('naked_triple')
                return True

        if self.hidden_triple(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('hidden_triple')
                return True

        if self.intersection_removal(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('intersection_removal')
                return True

        if self.special_intersection_removal(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('intersection_removal')
                return True

        if self.x_wing(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('x-wing')
                return True

        if self.y_wing(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('y-wing')
                return True

        if self.swordfish(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('swordfish')
                return True

        if self.xy_chain(sudoku):
            if self.__collect_report:
                return self.__report_json
            else:
                self.add_strategy_applied('xy-chain')
                return True

        if self.__collect_report:
            self.__report_json['text'] = _('Sudoku Helper nebyl schopen najít další logický krok. Toto může znamenat, '
                                           'že řešení neexistuje, nebo pouze že tento nástroj neumí tak složitou '
                                           'strategii, která by vedla k řešení.')
            self.__report_json['success'] = False
            return self.__report_json
        else:
            return False

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
        for i in range(4):
            if self.__cell_id_mapping[cell_id]['hypersudoku'][i]:
                extra_ids += self.__hyper_ids[i]

        # for row
        if sudoku.cells[cell_id].is_solved():
            num = sudoku.cells[cell_id].solved
            # for each other id in cells row block/col block/sector
            for cell_id_2 in (
                    self.__row_ids[row_id] + self.__col_ids[col_id] + self.__sector_ids[sector_id] + extra_ids):
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
                        'center': _('v centrech čtverců'),
                        'hypersudoku': _('v sektoru hypersudoku')
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
                                    'hypersudoku': _('tohoto sektoru hypersudoku'),
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
            for y in range(x + 1, info_list_len):
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
                                               'hypersudoku': _('v daném sektoru hypersudoku'),
                                               'diagonal_a': _('na dané diagonále'),
                                               'diagonal_b': _('na dané diagonále'),
                                               'center': _('mezi středy čtverců')
                                               }
                            self.__report_json['text'] = _('Buňky ' + ids_str + ' obsahují jako jediné ' +
                                                           location_mapper[
                                                               location] + ' kandidátní čísla ' + num_str + '(žlutě). Proto je v '
                                                                                                            'těchto buňkách možné odstranit všechna ostatní kandidátní čísla (červeně).')
                        return True
        return False

    # NAKED TRIPLE/QUAD - DONE
    def naked_triple(self, sudoku):
        return self.__apply_for_each(sudoku, self.naked_triple_on_one_block, 'block')

    def naked_triple_on_one_block(self, sudoku, ids_chunk, location):
        if self.__max_sudoku_number == 16:
            cells_info_list = collect_cell_candidates_info_list(sudoku, ids_chunk, limit=8)
            found_groups = naked_triple_check_for_groups(cells_info_list, is_hexa_sudoku=True)
        else:
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
                            'hypersudoku': _('v jednom sektoru hypersudoku'),
                            'diagonal_a': _('na jedné diagonále'),
                            'diagonal_b': _('na jedné diagonále'),
                            'center': _('ve středech čtverců')
                        }
                        self.__report_json['text'] = _('V buňkách ' + cell_pos_str + ' se nachází '
                                                                                     'stejná kandidátní čísla ' +
                                                       num_list_str + ' (žlutě) a jejich počet je roven '
                                                                      'počtu buněk, které zabírají. Protože leží všechny tyto buňky '
                                                       + location_mapper[location] + ', je možno tato ' +
                                                       'kandidátní čísla z ostatních buňek bloku odstranit (červeně).')
                    return True
        return False

    # HIDDEN TRIPLE/QUAD - DONE
    def hidden_triple(self, sudoku):
        return self.__apply_for_each(sudoku, self.hidden_triple_on_one_block, 'block')

    def hidden_triple_on_one_block(self, sudoku, ids_chunk, location):
        if self.__max_sudoku_number == 16:
            info_list = collect_candidate_occurences_info_list(sudoku, ids_chunk, limit=7)
            found_groups = hidden_triple_check_for_groups(info_list, is_hexa_sudoku=True)
        else:
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
                                       'hypersudoku': _('v daném sektoru hypersudoku'),
                                       'diagonal_a': _('na dané diagonále'),
                                       'diagonal_b': _('na dané diagonále'),
                                       'center': _('ve středech čtverců')
                                       }
                    self.__report_json['text'] = _('Buňky ' + ids_str + ' obsahují jako jediné ' +
                                                   location_mapper[
                                                       location] + ' kandidátní čísla ' + num_str + ' (žlutě). Proto je v'
                                                                                                    ' těchto buňkách možné odstranit všechna ostatní kandidátní čísla (červeně).')
                return True
        return False

    # INTERSECTION REMOVAL - DONE
    def intersection_removal(self, sudoku):
        return self.__apply_for_each(sudoku, self.intersection_removal_on_one_block, 'block')

    def intersection_removal_on_one_block(self, sudoku, ids_chunk, location):
        candidate_info_list = collect_candidate_occurences_info_list(sudoku, ids_chunk)
        for candidate_info_dict in candidate_info_list:
            candidates_forms = self.get_ids_group_block_names(candidate_info_dict['cell_ids'])
            for block_type in candidates_forms:
                if block_type == location:
                    continue  # candidate group from one block will have no effect on the same block
                # we have candidate which occurence intersects with another block and may change something there
                changed_something = self.project_intersection_on_another_block(sudoku, block_type, candidate_info_dict)
                if changed_something:
                    if self.__collect_report:
                        self.__report_json['success'] = True
                        self.__report_json['strategy_applied'] = 'intersection_removal'
                        for cell_id in candidate_info_dict['cell_ids']:
                            self.report_add_highlight(cell_id, False, 'yellow', candidate_info_dict['num'])
                        location_mapper = {
                            'row': _('v řádku'),
                            'col': _('v sloupci'),
                            'sector': _('v sektoru'),
                            'hypersudoku': _('v sektoru hypersudoku'),
                            'diagonal_a': _('na diagonále'),
                            'diagonal_b': _('na diagonále'),
                            'center': _('v středech čtverců')
                        }
                        location_mapper2 = {
                            'row': _('v stejném řádku'),
                            'col': _('v stejném sloupci'),
                            'sector': _('v stejném sektoru'),
                            'hypersudoku': _('v stejném sektoru hypersudoku'),
                            'diagonal_a': _('na stejné diagonále'),
                            'diagonal_b': _('na stejné diagonále'),
                            'center': _('v středech čtverců')
                        }
                        location_mapper3 = {
                            'row': _('v řádku'),
                            'col': _('v sloupci'),
                            'sector': _('v sektoru'),
                            'hypersudoku': _('v sektoru hypersudoku'),
                            'diagonal_a': _('na diagonále'),
                            'diagonal_b': _('na diagonále'),
                            'center': _('v středech čtverců')
                        }
                        self.__report_json['text'] = _('Číslo <b>' + str(candidate_info_dict['num']) + '</b> se ' +
                                                       location_mapper[location] + ' nachází pouze v buňkách ' +
                                                       self.get_multiple_bold_cell_pos_str(
                                                           candidate_info_dict['cell_ids']) +
                                                       ' (žlutě). Kromě tohoto bloku avšak buňky leží také ' +
                                                       location_mapper2[block_type] + '. Protože je jisté, že '
                                                                                      'číslice bude na jedné ze žlutě označených pozic, nemůže ' +
                                                       location_mapper3[block_type] +
                                                       ' být na jiné pozici a můžeme tato kandidátní čísla (označená'
                                                       ' červeně) odstranit.')
                    return True

    def project_intersection_on_another_block(self, sudoku, block_type, candidate_occurence_info_dict):
        # got pointing pair (info_dict) and block_type they could be pointing into
        # 1) find out ids of the block (reverse mapping)
        # 2) find out if there is candidate dict['num'] in between them
        changed_something = False
        block_ids = []
        one_candidate_occurence = candidate_occurence_info_dict['cell_ids'][0]
        # can map from any of them, at this point it's sure all of them are in this block
        if block_type == 'row':
            block_ids = self.__row_ids[self.__cell_id_mapping[one_candidate_occurence]['row_id']]
        elif block_type == 'col':
            block_ids = self.__col_ids[self.__cell_id_mapping[one_candidate_occurence]['col_id']]
        elif block_type == 'sector':
            block_ids = self.__sector_ids[self.__cell_id_mapping[one_candidate_occurence]['sector_id']]
        elif block_type == 'diagonal_a':
            block_ids = self.__diagonal_a_ids
        elif block_type == 'diagonal_b':
            block_ids = self.__diagonal_b_ids
        elif block_type == 'center':
            block_ids = self.__center_ids
        elif block_type == 'hypersudoku':
            for i in range(4):
                if one_candidate_occurence in self.__hyper_ids[i]:
                    block_ids = self.__hyper_ids[i]

        for cell_id in block_ids:
            if cell_id in candidate_occurence_info_dict['cell_ids']:
                continue  # skipping the same cells
            num = candidate_occurence_info_dict['num']
            if num in sudoku.cells[cell_id].notes:
                # found candidate this strategy WILL eliminate
                if self.__collect_report:
                    self.report_add_highlight(cell_id, False, 'red', num)
                    self.report_add_candidate_to_remove(cell_id, num)
                else:
                    sudoku.cells[cell_id].notes.remove(num)
                changed_something = True

        return changed_something

    # SPECIAL INTERSECTION REMOVAL
    def special_intersection_removal(self, sudoku):
        if self.__sudoku_type_name == 'diagonal' or self.__sudoku_type_name == 'diagonal_centers':
            if self.__apply_for_each(sudoku, self.special_intersection_removal_on_one_block, 'diagonal_a'):
                return True
        if self.__sudoku_type_name == 'diagonal' or self.__sudoku_type_name == 'diagonal_centers':
            if self.__apply_for_each(sudoku, self.special_intersection_removal_on_one_block, 'diagonal_b'):
                return True
        if self.__sudoku_type_name == 'centers' or self.__sudoku_type_name == 'diagonal_centers':
            if self.__apply_for_each(sudoku, self.special_intersection_removal_on_one_block, 'center'):
                return True
        if self.__sudoku_type_name == 'jigsaw':
            if self.__apply_for_each(sudoku, self.special_intersection_removal_on_one_block, 'sector'):
                return True

    def special_intersection_removal_on_one_block(self, sudoku, ids_chunk, location):
        candidate_info_list = collect_candidate_occurences_info_list(sudoku, ids_chunk)
        if location == 'diagonal_a':
            pass
        for candidate_info_dict in candidate_info_list:
            changed_something = False
            found_cells = []
            # for one number within this block
            for cell_id in range(0, self.__cell_id_limit):
                # for each cell in sudoku that is not from this block (ids_chunk),
                # is not solved and does contain the num
                if cell_id in ids_chunk:
                    continue
                if sudoku.cells[cell_id].is_solved():
                    continue
                if candidate_info_dict['num'] not in sudoku.cells[cell_id].notes:
                    continue

                sees_all = True
                for cell_to_see in candidate_info_dict['cell_ids']:
                    # to apply strategy, cell needs to see each cell in "cell_ids"
                    if not self.cells_in_same_block(cell_id, cell_to_see):
                        sees_all = False
                        break

                if sees_all:
                    # strategy can be applied
                    changed_something = True
                    if self.__collect_report:
                        found_cells.append(cell_id)
                        self.report_add_highlight(cell_id, False, 'red', candidate_info_dict['num'])
                        self.report_add_candidate_to_remove(cell_id, candidate_info_dict['num'])
                    else:
                        sudoku.celsl[cell_id].notes.remove(candidate_info_dict['num'])

            if changed_something:
                if self.__collect_report:
                    self.__report_json['success'] = True
                    self.__report_json['strategy_applied'] = 'intersection_removal'
                    for cell_id_in_block in candidate_info_dict['cell_ids']:
                        self.report_add_highlight(cell_id_in_block, False, 'yellow', candidate_info_dict['num'])
                    location_mapper = {
                        'diagonal_a': _('na diagonále'),
                        'diagonal_b': _('na diagonále'),
                        'centers': _('ve středech čtverců'),
                        'sector': _('v sektoru')
                    }
                    self.__report_json['text'] = _('Číslo <b>' + str(candidate_info_dict['num']) + '</b> se ' +
                                                   location_mapper[location] + ' nachází pouze v buňkách ' +
                                                   self.get_multiple_bold_cell_pos_str(candidate_info_dict['cell_ids'])
                                                   + ' (žlutě). ' + self.get_multiple_bold_cell_pos_str(found_cells) +
                                                   ' sdílí s každou z nich blok a proto odtud můžeme odstranit '
                                                   'kandidátní číslo ' + str(candidate_info_dict['num']) +
                                                   ' (červeně).')
                return True

        return False

    # X-WING DONE
    def x_wing(self, sudoku):
        found_groups = []
        for num in range(1, sudoku.max_sudoku_number + 1):
            found_groups += self.collect_one_number_for_x_wing(sudoku, self.__col_ids, 2, 'col', num)
            found_groups += self.collect_one_number_for_x_wing(sudoku, self.__row_ids, 2, 'row', num)

        if len(found_groups) != 0:
            # found some groups fro x-wing, now only need to determine whether they make a change
            for one_group in found_groups:
                changed_something = False
                for effect_location_id in one_group['effect_location_ids']:
                    if one_group['location'] == 'row':
                        effect_block = self.__col_ids[effect_location_id]
                    else:
                        effect_block = self.__row_ids[effect_location_id]
                    # test each cell in location for canddiates to remove
                    for cell_id in effect_block:
                        if cell_id in one_group['cell_ids']:
                            continue  # skip those that are part of a strategy
                        if one_group['num'] in sudoku.cells[cell_id].notes:
                            # found canddiate to remove
                            changed_something = True
                            if self.__collect_report:
                                self.report_add_highlight(cell_id, False, 'red', one_group['num'])
                                self.report_add_candidate_to_remove(cell_id, one_group['num'])
                            else:
                                sudoku.cells[cell_id].notes.remove(one_group['num'])

                # here after checking all effects of one group
                if changed_something:
                    if self.__collect_report:
                        self.__report_json['success'] = True
                        self.__report_json['strategy_applied'] = 'x-wing'
                        for cell_id in one_group['cell_ids']:
                            self.report_add_highlight(cell_id, False, 'yellow', one_group['num'])
                        location_mapper1 = {
                            'row': _('v těchto dvou řádcích'),
                            'col': _('v těchto dvou sloupcích')
                        }
                        location_mapper2 = {
                            'col': _('v jejich řádcích'),
                            'row': _('v jejich sloupcích')
                        }
                        self.__report_json['text'] = _('Žlutě označené buňky ' +
                                                       self.get_multiple_bold_cell_pos_str(one_group['cell_ids']) +
                                                       ' obsahují jediné výskyty <b>' + str(one_group['num']) + '</b> '
                                                                                                                ' ' +
                                                       location_mapper1[one_group['location']] + '. Je proto '
                                                                                                 'jisté, že ' + str(
                            one_group['num']) + ' bude na dvou z těchto '
                                                'pozic a nemůže být nikde jinde ' +
                                                       location_mapper2[one_group['location']] + ' (červeně).')
                    return True

        return False

    def collect_one_number_for_x_wing(self, sudoku, ids_list, limit, location, num):
        # collect information from onyl those numbers that are 2-3 (or just 2 for limit 2) times in a ids_list
        block_occurence = []
        for ids_chunk in ids_list:
            occurence_cells = []
            occurence_block_ids = []
            for cell_id in ids_chunk:
                if num in sudoku.cells[cell_id].notes:
                    # append cell_id and col/row id
                    if location == 'col':
                        occurence_block_ids.append(self.__cell_id_mapping[cell_id]['row_id'])
                        occurence_cells.append(cell_id)
                    else:
                        # location == 'row'
                        occurence_block_ids.append(self.__cell_id_mapping[cell_id]['col_id'])
                        occurence_cells.append(cell_id)
            block_occurence.append((occurence_cells, occurence_block_ids))

        found_groups = []

        # cross compare 2
        for block_id_1 in range(0, len(block_occurence)):
            for block_id_2 in range(block_id_1 + 1, len(block_occurence)):
                if limit == 2:
                    group = is_group_of_same_numbers([block_occurence[block_id_1][1], block_occurence[block_id_2][1]])
                    if group is not None:
                        found_groups.append({
                            'num': num,
                            'location': location,
                            'cell_ids': block_occurence[block_id_1][0] + block_occurence[block_id_2][0],
                            'effect_location_ids': list(group)
                        })
                # cross compare 3 if limit is 3
                if limit == 3:
                    for block_id_3 in range(block_id_2 + 1, len(block_occurence)):
                        group = is_group_of_same_numbers(
                            [block_occurence[block_id_1][1], block_occurence[block_id_2][1],
                             block_occurence[block_id_3][1]])
                        if group is not None:
                            found_groups.append({
                                'num': num,
                                'location': location,
                                'cell_ids': block_occurence[block_id_1][0] + block_occurence[block_id_2][0]
                                            + block_occurence[block_id_3][0],
                                'effect_location_ids': list(group)
                            })

        return found_groups

    # Y-WING DONE
    def y_wing(self, sudoku):
        chain_map = self.get_chain_mapping(sudoku)
        already_tested = []
        for chain_id in chain_map.keys():
            possible_chains = self.get_possibly_y_wings_from_cell(sudoku, chain_map, chain_id)
            for possible_chain in possible_chains:
                if ((possible_chain['wing_a_id'], possible_chain['wing_b_id'], possible_chain['leftover'])
                        in already_tested or (possible_chain['wing_b_id'], possible_chain['wing_a_id'],
                                              possible_chain['leftover']) in already_tested):
                    continue  # this combo was already tested
                already_tested.append(((possible_chain['wing_a_id'], possible_chain['wing_b_id'],
                                        possible_chain['leftover'])))

                changed_something = False
                for cell_id in range(0, self.__cell_id_limit):
                    # for each cell in sudoku, check if it "sees" two ends is made
                    if (cell_id == possible_chain['middle_cell_id'] or cell_id == possible_chain['wing_a_id'] or
                            cell_id == possible_chain['wing_b_id']):
                        continue  # skip check for cells that are part of the chain
                    if sudoku.cells[cell_id].is_solved():
                        continue  # skip for solved cells

                    # check if cells sees both wings
                    if (self.cells_in_same_block(cell_id, possible_chain['wing_a_id']) and
                            self.cells_in_same_block(cell_id, possible_chain['wing_b_id'])):
                        if possible_chain['leftover'] in sudoku.cells[cell_id].notes:
                            # candidate can be removed!
                            changed_something = True
                            if self.__collect_report:
                                self.report_add_highlight(cell_id, False, 'red', possible_chain['leftover'])
                                self.report_add_candidate_to_remove(cell_id, possible_chain['leftover'])
                            else:
                                sudoku.cells[cell_id].notes.remove(possible_chain['leftover'])

                if changed_something:
                    # strategy success, note evertyhting and return True
                    if self.__collect_report:
                        self.__report_json['success'] = True
                        self.__report_json['strategy_applied'] = 'y-wing'
                        self.report_add_highlight(possible_chain['wing_a_id'], False, 'yellow',
                                                  possible_chain['leftover'])
                        self.report_add_highlight(possible_chain['wing_b_id'], False, 'yellow',
                                                  possible_chain['leftover'])
                        self.report_add_highlight(possible_chain['wing_a_id'], False, 'green',
                                                  possible_chain['connection_a'])
                        self.report_add_highlight(possible_chain['wing_b_id'], False, 'green',
                                                  possible_chain['connection_b'])
                        self.report_add_highlight(possible_chain['middle_cell_id'], False, 'green',
                                                  possible_chain['connection_a'])
                        self.report_add_highlight(possible_chain['middle_cell_id'], False, 'green',
                                                  possible_chain['connection_b'])
                        self.report_add_chain(possible_chain['wing_a_id'], possible_chain['connection_a'],
                                              possible_chain['middle_cell_id'], possible_chain['connection_a'])
                        self.report_add_chain(possible_chain['wing_b_id'], possible_chain['connection_b'],
                                              possible_chain['middle_cell_id'], possible_chain['connection_b'])
                        self.__report_json['text'] = _('Zeleně je zvýrazněno nalezené Y-Wing. Na jeho koncích se '
                                                       'nachází <b>' + str(possible_chain['leftover']) + ' </b> '
                                                                                                         '(žlutě) a na jedné z těchto pozic musí být. Lze odstranit '
                                                                                                         'kandidátní číslo' + str(
                            possible_chain['leftover']) + ' ze '
                                                          'všech pozic (červeně), které sdílí libovolný blok s oběma konci'
                                                          ' Y-Wing.')

                    return True

        return False

    def get_chain_mapping(self, sudoku):
        chain_map = {}
        for cell_id in range(0, self.__cell_id_limit):
            if not sudoku.cells[cell_id].is_solved() and len(sudoku.cells[cell_id].notes) == 2:
                row_id, col_id, sector_id = self.get_row_col_sector_id_of_cell(cell_id)
                extra_ids = []
                if self.__cell_id_mapping[cell_id]['diagonal_a']:
                    extra_ids += self.__diagonal_a_ids
                if self.__cell_id_mapping[cell_id]['diagonal_b']:
                    extra_ids += self.__diagonal_b_ids
                if self.__cell_id_mapping[cell_id]['center']:
                    extra_ids += self.__center_ids
                for i in range(4):
                    if self.__cell_id_mapping[cell_id]['hypersudoku'][i]:
                        extra_ids += self.__hyper_ids[i]
                for cell_id_2 in (self.__row_ids[row_id] + self.__col_ids[col_id] +
                                  self.__sector_ids[sector_id] + extra_ids):
                    if (sudoku.cells[cell_id_2].is_solved() or len(sudoku.cells[cell_id_2].notes) != 2
                            or cell_id_2 == cell_id):
                        continue  # skip solved cells and cells with more than 2 candidates and cells with same id

                    if cell_id not in chain_map:
                        chain_map[cell_id] = []
                    if cell_id_2 not in chain_map[cell_id]:
                        chain_map[cell_id].append(cell_id_2)

        return chain_map

    def get_possibly_y_wings_from_cell(self, sudoku, chain_map, cell_id):
        possible_chains = []
        for possible_way_id in chain_map[cell_id]:
            # for each cell with 2 candidates it is in one block with
            connected_by = []
            for num in sudoku.cells[cell_id].notes:
                if num in sudoku.cells[possible_way_id].notes:
                    connected_by.append(num)  # checks if the cells share number

            for num in connected_by:
                end_a_leftover = select_the_other_note_on_two_note_cell(sudoku, cell_id, num)
                # for possible connection to possible_way_id checks for another link
                for possible_end_id in chain_map[possible_way_id]:
                    if possible_end_id == cell_id:
                        continue  # skip self
                    connection = select_the_other_note_on_two_note_cell(sudoku, possible_way_id, num)
                    if connection in sudoku.cells[possible_end_id].notes:
                        # at this point, it is clear
                        end_b_leftover = select_the_other_note_on_two_note_cell(sudoku, possible_end_id, connection)
                        if end_a_leftover == end_b_leftover:
                            possible_chains.append({
                                'middle_cell_id': possible_way_id,
                                'wing_a_id': cell_id,
                                'wing_b_id': possible_end_id,
                                'connection_a': num,
                                'connection_b': connection,
                                'leftover': end_a_leftover
                            })
        return possible_chains

    # SWORDFISH - DONE
    def swordfish(self, sudoku):
        found_groups = []
        for num in range(1, sudoku.max_sudoku_number + 1):
            found_groups += self.collect_one_number_for_x_wing(sudoku, self.__col_ids, 3, 'col', num)
            found_groups += self.collect_one_number_for_x_wing(sudoku, self.__row_ids, 3, 'row', num)

        if len(found_groups) != 0:
            # found some groups fro x-wing, now only need to determine whether they make a change
            for one_group in found_groups:
                changed_something = False
                for effect_location_id in one_group['effect_location_ids']:
                    if one_group['location'] == 'row':
                        effect_block = self.__col_ids[effect_location_id]
                    else:
                        effect_block = self.__row_ids[effect_location_id]
                    # test each cell in location for canddiates to remove
                    for cell_id in effect_block:
                        if cell_id in one_group['cell_ids']:
                            continue  # skip those that are part of a strategy
                        if one_group['num'] in sudoku.cells[cell_id].notes:
                            # found canddiate to remove
                            changed_something = True
                            if self.__collect_report:
                                self.report_add_highlight(cell_id, False, 'red', one_group['num'])
                                self.report_add_candidate_to_remove(cell_id, one_group['num'])
                            else:
                                sudoku.cells[cell_id].notes.remove(one_group['num'])

                # here after checking all effects of one group
                if changed_something:
                    if self.__collect_report:
                        self.__report_json['success'] = True
                        self.__report_json['strategy_applied'] = 'swordfish'
                        for cell_id in one_group['cell_ids']:
                            self.report_add_highlight(cell_id, False, 'yellow', one_group['num'])
                        location_mapper1 = {
                            'row': _('v těchto třech řádcích'),
                            'col': _('v těchto třech sloupcích')
                        }
                        location_mapper2 = {
                            'col': _('v jejich řádcích'),
                            'row': _('v jejich sloupcích')
                        }
                        self.__report_json['text'] = _('Žlutě označené buňky ' +
                                                       self.get_multiple_bold_cell_pos_str(one_group['cell_ids']) +
                                                       ' obsahují jediné výskyty <b>' + str(one_group['num']) + '</b> '
                                                       + location_mapper1[one_group['location']] + '. Je proto '
                                                                                                   'jisté, že ' + str(
                            one_group['num']) + ' bude na třech z těchto '
                                                'pozic a nemůže být nikde jinde ' +
                                                       location_mapper2[one_group['location']] + ' (červeně).')
                    return True

        return False

    # XY-CHAIN DONE
    def xy_chain(self, sudoku):
        chain_map = self.get_chain_mapping(sudoku)
        already_tested = []
        for chain_id in chain_map.keys():
            possible_chains = self.get_possible_chains(sudoku, chain_map, chain_id)
            for possible_chain in possible_chains:
                # for each possible chain - chain of 3+ cells that end with same candidate, but may not eliminate
                # anything
                if ((possible_chain['chain_ids'][0], possible_chain['chain_ids'][-1], possible_chain['leftover'])
                        in already_tested or (possible_chain['chain_ids'][-1], possible_chain['chain_ids'][0],
                                              possible_chain['leftover']) in already_tested):
                    continue  # this combo was already tested

                already_tested.append((possible_chain['chain_ids'][0], possible_chain['chain_ids'][-1],
                                       possible_chain['leftover']))

                changed_something = False
                for cell_id in range(0, self.__cell_id_limit):
                    # for each cell in sudoku, check if it "sees" two ends
                    if cell_id in possible_chain['chain_ids']:
                        continue  # skip cells that form the strategy
                    if sudoku.cells[cell_id].is_solved():
                        continue  # skip solved

                    # check if it "sees" two ends
                    if (self.cells_in_same_block(cell_id, possible_chain['chain_ids'][0]) and
                            self.cells_in_same_block(cell_id, possible_chain['chain_ids'][-1])):
                        if possible_chain['leftover'] in sudoku.cells[cell_id].notes:
                            # canddiate can be removed
                            changed_something = True
                            if self.__collect_report:
                                self.report_add_highlight(cell_id, False, 'red', possible_chain['leftover'])
                                self.report_add_candidate_to_remove(cell_id, possible_chain['leftover'])
                            else:
                                sudoku.cells[cell_id].notes.remove(int(possible_chain['leftover']))

                if changed_something:
                    # strategy success, note everything and return True
                    if self.__collect_report:
                        self.__report_json['success'] = True
                        self.__report_json['strategy_applied'] = 'xy-chain'
                        for i, connection in enumerate(possible_chain['connections']):
                            self.report_add_highlight(possible_chain['chain_ids'][i], False, 'green', connection)
                            self.report_add_highlight(possible_chain['chain_ids'][i + 1], False, 'green', connection)
                            self.report_add_chain(possible_chain['chain_ids'][i], connection,
                                                  possible_chain['chain_ids'][i + 1], connection)
                        self.report_add_highlight(possible_chain['chain_ids'][0], False, 'yellow',
                                                  possible_chain['leftover'])
                        self.report_add_highlight(possible_chain['chain_ids'][-1], False, 'yellow',
                                                  possible_chain['leftover'])
                        self.__report_json['text'] = _('Zeleně je zvýrazněn nalezený XY-Chain. Na jeho koncích se'
                                                       'nachází <b>' + str(possible_chain['leftover']) + ' </b> '
                                                                                                         '(žlutě) a na jedné z těchto pozic musí být. Lze odstranit '
                                                                                                         'kandidátní číslo' + str(
                            possible_chain['leftover']) + ' ze '
                                                          'všech pozic (červeně), které sdílí libovolný blok s oběma konci'
                                                          ' XY-Chain.')
                    return True

        return False

    def get_possible_chains(self, sudoku, chain_map, cell_id):
        possible_chains = []

        for possible_way_id in chain_map[cell_id]:
            # for each cell with 2 candidates it is in one block with
            connected_by = []
            for num in sudoku.cells[cell_id].notes:
                if num in sudoku.cells[possible_way_id].notes:
                    connected_by.append(num)  # checks if the cells share number

            for num in connected_by:
                chain_in_making = {
                    'chain_ids': [cell_id, possible_way_id],
                    'connections': [num],
                    'leftover': select_the_other_note_on_two_note_cell(sudoku, cell_id, num)
                }

                possible_chains += self.chain_search(sudoku, chain_map, possible_way_id, chain_in_making)

        return possible_chains

    def chain_search(self, sudoku, chain_map, cell_id, chain_in_making):
        possible_chains = []
        new_connection = select_the_other_note_on_two_note_cell(sudoku, cell_id, chain_in_making['connections'][-1])
        # check if this chain is closed off and is at least 4 in lenght
        # (2 is naked pair, 3 is y-wing, both aready tested)
        if new_connection == chain_in_making['leftover'] and len(chain_in_making['chain_ids']) > 3:
            possible_chains.append(chain_in_making)

        for possible_way_id in chain_map[cell_id]:
            # check if not already part of it
            if possible_way_id in chain_in_making['chain_ids']:
                continue

            if new_connection in sudoku.cells[possible_way_id].notes:
                new_chain_in_making = copy.deepcopy(chain_in_making)
                new_chain_in_making['chain_ids'].append(possible_way_id)
                new_chain_in_making['connections'].append(new_connection)
                possible_chains += self.chain_search(sudoku, chain_map, possible_way_id, new_chain_in_making)

        return possible_chains

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, redirect
import django.template.loader
from django.template import TemplateDoesNotExist
from django.template.defaultfilters import register
from django.utils.translation import gettext as _
import json

from utils.strategy_manager import StrategyApplier
from utils.sudoku_convertor import convert_js_json_to_sudoku_board, convert_sudoku_board_to_simple_array
from utils.generator import Generator

# Variable that allows showing of extra controls such as custom highlights for
developers_tools = False

# === STRATEGY SUPPORTING VARIABLES ===
easy_strategies = {
    'remove_collisions': _('Odstranění přímých kolizí'),
    'naked_single': 'Naked Single',
    'hidden_single': 'Hidden Single',
    'naked_pair': 'Naked Pair',
    'hidden_pair': 'Hidden Pair',
    'naked_triple': 'Naked Triple+',
    'hidden_triple': 'Hidden Triple+'
}

advanced_strategies = {
    'intersection_removal': 'Intersection Removal',
    'x-wing': 'X-Wing',
    'y-wing': 'Y-Wing',
    'swordfish': 'Swordfish',
    'xy-chain': 'XY-Chain'
}

strategies_context = {'easy_strategies': easy_strategies,
                      'advanced_strategies': advanced_strategies,
                      'developers_tools': developers_tools}

# === SOLVER SUPPORTING VARIABLES ===
basic_sudokus = {
    'sudoku4x4': 'Sudoku 4x4',
    'sudoku6x6': 'Sudoku 6x6',
    'sudoku9x9': 'Sudoku 9x9',
    'sudoku16x16': 'Sudoku 16x16'
}
extra_rules = {
    'diagonal': _('Diagonální sudoku'),
    'centers': _('Sudoku se středy čtverců'),
    'diagonal_centers': _('Diagonální sudoku se středy čtverců'),
    'jigsaw': 'Jigsaw',
    'hypersudoku': 'Hypersudoku'
}
math_sudokus = {

}
sudokus_context = {'basic_sudokus': basic_sudokus,
                   'extra_rules': extra_rules,
                   'math_sudokus': math_sudokus,
                   'max_sudoku_number': 9,
                   'developers_tools': developers_tools}

max_sudoku_numbers = {'sudoku4x4': 4,
                      'sudoku6x6': 6,
                      'sudoku9x9': 9,
                      'sudoku16x16': 16}
sudoku_template_mapper = {'sudoku4x4': 'classic_sudoku_grid',
                          'sudoku6x6': 'classic_sudoku_grid',
                          'sudoku9x9': 'classic_sudoku_grid',
                          'sudoku16x16': 'classic_sudoku_grid',
                          'diagonal': 'special_cells_sudoku_grid',
                          'centers': 'special_cells_sudoku_grid',
                          'diagonal_centers': 'special_cells_sudoku_grid',
                          'jigsaw': 'jigsaw_sudoku_grid',
                          'hypersudoku': 'special_cells_sudoku_grid'}
sudoku_type_mapper = {'sudoku4x4': 'classic',
                      'sudoku6x6': 'classic',
                      'sudoku9x9': 'classic',
                      'sudoku16x16': 'classic',
                      'diagonal': 'diagonal',
                      'centers': 'centers',
                      'diagonal_centers': 'diagonal_centers',
                      'jigsaw': 'jigsaw',
                      'hypersudoku': 'hypersudoku'}

@register.filter
def get_range(val):
    return range(val)

@register.filter
def get_cell_num(x, y):
    return x + y

@register.filter
def mul(a, b):
    return a * b

@register.filter
def break_for_keyboard(a, max_sudoku_num):
    if max_sudoku_num == 4:
        div = 2
    elif max_sudoku_num == 6:
        div = 2
    elif max_sudoku_num == 16:
        div = 4
    else:
        div = 3
    return (a % div) == 0

@register.filter
def get_note_x(max_sudoku_num):
    if max_sudoku_num == 4:
        return 2
    if max_sudoku_num == 6:
        return 2
    if max_sudoku_num == 16:
        return 4
    return 3

@register.filter
def get_note_y(max_sudoku_num):
    if max_sudoku_num == 4:
        return 2
    if max_sudoku_num == 6:
        return 3
    if max_sudoku_num == 16:
        return 4
    return 3

@register.filter
def get_width_percentage(max_sudoku_num):
    if max_sudoku_num == 4:
        return 33
    if max_sudoku_num == 6:
        return 40
    if max_sudoku_num == 16:
        return 25
    return 33

@register.filter
def transform_to_letter_if_needed(num):
    if num < 10:
        return num
    return chr(int(num) + 55)

@register.filter
def add_prev_strategies(curr_counter, prev_strategies_dict):
    return curr_counter + len(prev_strategies_dict)

@register.filter
def is_diagonal(x, y):
    if x == y or x == (8 - y):
        return "special-sudoku-cell"
    return ""

@register.filter
def is_diagonal_or_center(x, y):
    if (x in [1, 4, 7] and y in [1, 4, 7]) or x == y or x == (8 - y):
        return "special-sudoku-cell"
    return ""

@register.filter
def is_center(x, y):
    if x in [1, 4, 7] and y in [1, 4, 7]:
        return "special-sudoku-cell"
    return ""

@register.filter
def is_hyper_cell(x, y):
    if x in [1, 2, 3, 5, 6, 7] and y in [1, 2, 3, 5, 6, 7]:
        return "special-sudoku-cell"
    return ""

def index(request):
    return render(request, 'index.html')


# ====================================
#           SOLVER VIEWS
# ====================================

def solver_index(request):
    return render(request, 'solver/index.html', sudokus_context)

def solver(request, name):
    try:
        template = 'solver/' + sudoku_template_mapper[name] + '.html'
    except KeyError:
        raise Http404(_('Aplikace na řešení') + ' "' + name + '" ' + _('nebyla nalezena.'))

    custom_context = sudokus_context.copy()
    custom_context['sudoku_name'] = name
    if name in basic_sudokus:
        custom_context['sudoku_name_to_display'] = basic_sudokus[name]
    elif name in extra_rules:
        custom_context['sudoku_name_to_display'] = extra_rules[name]
    elif name in math_sudokus:
        custom_context['sudoku_name_to_display'] = math_sudokus[name]

    if name in max_sudoku_numbers.keys():
        custom_context['max_sudoku_number'] = max_sudoku_numbers[name]

    # retrieving settings from session
    setting_shift_is_toggle = request.session.get('setting_shift_is_toggle', True)
    setting_sudoku_full_size = request.session.get('setting_sudoku_full_size', False)
    setting_show_keyboard = request.session.get('setting_show_keyboard', True)

    custom_context['setting_shift_is_toggle'] = setting_shift_is_toggle
    custom_context['setting_sudoku_full_size'] = setting_sudoku_full_size
    custom_context['setting_show_keyboard'] = setting_show_keyboard

    if name == 'sudoku4x4':
        # creating custom strategies from 4x4 sudoku
        custom_context['easy_strategies'] = {
            'remove_collisions': _('Odstranění přímých kolizí'),
            'naked_single': 'Naked Single',
            'hidden_single': 'Hidden Single',
            'naked_pair': 'Naked Pair'
        }
    else:
        custom_context['easy_strategies'] = easy_strategies
        custom_context['advanced_strategies'] = advanced_strategies
    try:
        request.session['max_sudoku_number'] = max_sudoku_numbers[name]
    except KeyError:
        request.session['max_sudoku_number'] = 9
    request.session['sudoku_type'] = sudoku_type_mapper[name]

    dont_check_jigsaw_sectors = False

    load_from = request.GET.get('load_from', None)
    cells = request.GET.get('cells', None)
    if cells is not None and load_from is not None:
        if name == 'jigsaw':
            jigsaw_sectors = request.GET.get('jigsaw_sectors', None)
            jigsaw_cell_sectors = request.GET.get('jigsaw_cell_sectors', None)
            custom_context['jigsaw_sectors'] = jigsaw_sectors
            custom_context['jigsaw_cell_sectors'] = jigsaw_cell_sectors
            request.session['jigsaw_sectors'] = json.loads(jigsaw_sectors)
            request.session['jigsaw_cell_sectors'] = json.loads(jigsaw_cell_sectors)
            dont_check_jigsaw_sectors = True
        custom_context['load_sudoku'] = load_from
        custom_context['cells'] = cells

    if name == 'jigsaw' and not dont_check_jigsaw_sectors:
        jigsaw_sectors = request.session.get('jigsaw_sectors', None)
        jigsaw_cell_sectors = request.session.get('jigsaw_cell_sectors', None)
        if jigsaw_sectors is None or jigsaw_cell_sectors is None:
            return redirect('/solver/edit_jigsaw_shape')
        custom_context['jigsaw_sectors'] = jigsaw_sectors
        custom_context['jigsaw_cell_sectors'] = jigsaw_cell_sectors

    seen_name = 'seen_' + name
    seen_this = request.session.get(seen_name, False)
    request.session[seen_name] = True
    custom_context['seen_this'] = seen_this

    return render(request, template, custom_context)

def edit_jigsaw_shape(request):
    if request.method == 'POST':
        sector_ids = json.loads(request.POST.get('sector_ids'))
        cell_sectors = json.loads(request.POST.get('cell_sectors'))
        request.session['jigsaw_sectors'] = sector_ids
        request.session['jigsaw_cell_sectors'] = cell_sectors
        return HttpResponse('ok')
    else:
        return render(request, 'solver/edit_jigsaw_shape.html')


def update_setting(request):
    setting = request.POST.get('setting')
    value = request.POST.get('value')
    if (setting == 'setting_shift_is_toggle' or setting == 'setting_sudoku_full_size'
            or setting == 'setting_show_keyboard'):
        request.session[setting] = (value.lower() == 'true')
    return HttpResponse('ok')

# ======== HINTS AND STEPS by strategies ==========

def get_next_step(request):
    sudoku_json = json.loads(request.POST.get('json'))
    sudoku = convert_js_json_to_sudoku_board(sudoku_json)

    sudoku_type_name = request.session.get('sudoku_type')

    if sudoku_type_name == "jigsaw":
        strategy_applier = StrategyApplier(request.session.get('max_sudoku_number'), sudoku_type_name,
                                           sector_ids=request.session.get('jigsaw_sectors'))
    else:
        strategy_applier = StrategyApplier(request.session.get('max_sudoku_number'), sudoku_type_name)
    result_json = strategy_applier.find_next_step(sudoku)

    return HttpResponse(json.dumps(result_json))

def generate_sudoku(request):
    sudoku_type_name = request.session.get('sudoku_name')
    if sudoku_type_name == "jigsaw":
        generator = Generator(request.session.get('max_sudoku_number'), sudoku_type_name,
                                           sector_ids=request.session.get('jigsaw_sectors'))
    else:
        generator = Generator(request.session.get('max_sudoku_number'), sudoku_type_name)
    sudoku = generator.generate()
    generator.create_sudoku(sudoku)
    array_sudoku = convert_sudoku_board_to_simple_array(sudoku)
    return HttpResponse(json.dumps({'success': True, 'sudoku': array_sudoku}))

def check_solvability(request):
    sudoku_json = json.loads(request.POST.get('json'))
    sudoku_for_part1 = convert_js_json_to_sudoku_board(sudoku_json)

    sudoku_type_name = request.session.get('sudoku_type')

    if sudoku_type_name == "jigsaw":
        strategy_applier = StrategyApplier(request.session.get('max_sudoku_number'), sudoku_type_name,
                                           sector_ids=request.session.get('jigsaw_sectors'), collect_report=False)
    else:
        strategy_applier = StrategyApplier(request.session.get('max_sudoku_number'), sudoku_type_name,
                                           collect_report=False)

    # test for collisions from user
    collisions = strategy_applier.has_obvious_mistakes(sudoku_for_part1)
    if collisions is not None:
        return HttpResponse(json.dumps({'result': _('V sudoku se nachází vyplněná číslice v přímé kolizi. '
                                           'Sudoku není vyřešitelné. Kolize na pozicích: ' + collisions)}))
    # test if solved to avoid needless proccessing
    if sudoku_for_part1.is_fully_solved():
        return HttpResponse(json.dumps({'result': _('Sudoku již vyřešeno, není co ověřovat.')}))


    result_dict = {}

    while True:
        if sudoku_for_part1.is_fully_solved():
            hardest_strategy = strategy_applier.get_hardest_strategy_applied()
            if hardest_strategy in easy_strategies:
                hardest_strategy = easy_strategies[hardest_strategy]
            elif hardest_strategy in advanced_strategies:
                hardest_strategy = advanced_strategies[hardest_strategy]
            result_dict['result'] = _('Logický postup dané sudoku dokázal vyřešit. Nejtěžší použitá strategie'
                                    ' (podle pořadí uváděném na této stránce) byla "' + hardest_strategy + '".')
            break
        if not strategy_applier.find_next_step(sudoku_for_part1):
            result_dict['result'] = _('Logický postup na zadaném sudoku selhal. Doplnili jste možná kandidáty do '
                                      'prázdných buněk před stiskem tlačítka?')
            break

    return HttpResponse(json.dumps(result_dict))

# ====================================
#           GUIDES VIEWS
# ====================================

def guides_index(request):
    return render(request, 'guides/index.html', strategies_context)


def detail(request, name):
    template = 'guides/' + name + '.html'
    try:
        django.template.loader.get_template(template)
    except TemplateDoesNotExist:
        raise Http404(_('Návod') + ' "' + name + '" ' + _('nebyl nalezen.'))

    return render(request, template, strategies_context)

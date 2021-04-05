from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
import django.template.loader
from django.template import TemplateDoesNotExist
from django.template.defaultfilters import register
from django.utils.translation import gettext as _
import json

from utils.strategy_manager import StrategyApplier
from utils.sudoku_convertor import convert_js_json_to_sudoku_board

# Variable that allows showing of extra controls such as custom highlights for
developers_tools = True

# === STRATEGY SUPPORTING VARIABLES ===
easy_strategies = {
    'remove_collisions': _('Odstranění přímých kolizí'),
    'naked_single': 'Naked Single',
    'hidden_single': 'Hidden Single',
    'naked_pair': 'Naked Pair',
    'hidden_pair': 'Hidden Pair',
    'naked_triple': 'Naked Triple/Quad',
    'hidden_triple': 'Hidden Triple/Quad'
}
# TODO pro sudoku 16x16 musí jít hidden/naked až po 5-6-7-8čky
medium_strategies = {
    'intersection_removal': _('Intersection Removal')  # TODO not final name
}
advanced_strategies = {}
strategies_context = {'easy_strategies': easy_strategies,
                      'medium_strategies': medium_strategies,
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
                          'sudoku16x16': 'classic_sudoku_grid'}
sudoku_type_mapper = {'sudoku4x4': 'classic',
                      'sudoku6x6': 'classic',
                      'sudoku9x9': 'classic',
                      'sudoku16x16': 'classic'}

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
def add_prev_strategies_medium(counter):
    return counter + len(easy_strategies)

def index(request):
    return render(request, 'index.html')

# ====================================
#           SOLVER VIEWS
# ====================================

def solver_index(request):
    return render(request, 'solver/index.html', sudokus_context)

def solver(request, name):
    template = 'solver/' + sudoku_template_mapper[name] + '.html'
    try:
        django.template.loader.get_template(template)
    except TemplateDoesNotExist:
        raise Http404(_('Aplikace na řešení') + ' "' + name + '" ' + _('nebyla nalezena.'))

    custom_context = sudokus_context.copy()

    if name in max_sudoku_numbers.keys():
        custom_context['max_sudoku_number'] = max_sudoku_numbers[name]

    # retrieving settings from session
    setting_shift_is_toggle = request.session.get('setting_shift_is_toggle', True)
    setting_sudoku_full_size = request.session.get('setting_sudoku_full_size', False)

    custom_context['setting_shift_is_toggle'] = setting_shift_is_toggle
    custom_context['setting_sudoku_full_size'] = setting_sudoku_full_size

    custom_context['easy_strategies'] = easy_strategies
    custom_context['medium_strategies'] = medium_strategies
    custom_context['advanced_strategies'] = advanced_strategies

    request.session['max_sudoku_number'] = max_sudoku_numbers[name]
    request.session['sudoku_type'] = sudoku_type_mapper[name]

    return render(request, template, custom_context)

def update_setting(request):
    setting = request.POST.get('setting')
    value = request.POST.get('value')
    if (setting == 'setting_shift_is_toggle' or setting == 'setting_sudoku_full_size'):
        request.session[setting] = (value.lower() == 'true')
    return HttpResponse('ok')

# ======== HINTS AND STEPS by strategies ==========

def get_next_step(request):
    sudoku_json = json.loads(request.POST.get('json'))
    sudoku = convert_js_json_to_sudoku_board(sudoku_json)
    strategy_applier = StrategyApplier(request.session.get('max_sudoku_number'), request.session.get('sudoku_type'))
    result_json = strategy_applier.find_next_step(sudoku)

    return HttpResponse(json.dumps(result_json))

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

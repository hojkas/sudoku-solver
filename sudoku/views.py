from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
import django.template.loader
from django.template import TemplateDoesNotExist
from django.template.defaultfilters import register
from django.utils.translation import gettext as _
import json

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
medium_strategies = {}
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
                      'sudoku16x16': 16}
sudoku_template_mapper = {'sudoku4x4': 'classic_sudoku_grid',
                          'sudoku6x6': 'classic_sudoku_grid',
                          'sudoku9x9': 'classic_sudoku_grid',
                          'sudoku16x16': 'classic_sudoku_grid'}

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
    setting_show_collisions = request.session.get('setting_show_collisions', False)
    setting_sudoku_full_size = request.session.get('setting_sudoku_full_size', False)

    custom_context['setting_show_collisions'] = setting_show_collisions
    custom_context['setting_shift_is_toggle'] = setting_shift_is_toggle
    custom_context['setting_sudoku_full_size'] = setting_sudoku_full_size

    custom_context['easy_strategies'] = easy_strategies
    custom_context['medium_strategies'] = medium_strategies
    custom_context['advanced_strategies'] = advanced_strategies

    return render(request, template, custom_context)

def update_setting(request):
    setting = request.POST.get('setting')
    value = request.POST.get('value')
    if (setting == 'setting_show_collisions' or setting == 'setting_shift_is_toggle'
            or setting == 'setting_sudoku_full_size'):
        request.session[setting] = (value.lower() == 'true')
    return HttpResponse('ok')

# ======== HINTS AND STEPS by strategies ==========

def get_next_step(request):
    test_json = {
        "strategy_applied": "naked_pair",
        "success": True,
        "text": "I am<br>two-lined text",
        "highlight": [
            {
                "cell_id": 0,
                "is_solved": True,
                "note_id": None,
                "color": "green"
            },
            {
                "cell_id": 1,
                "is_solved": False,
                "note_id": 5,
                "color": "red"
            }
        ],
        "candidates_to_remove": [
            {
                "cell_id": 0,
                "note_id": 5
            }
        ]
    }

    return HttpResponse(json.dumps(test_json))

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

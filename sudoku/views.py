from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
import django.template.loader
from django.template import TemplateDoesNotExist
from django.template.defaultfilters import register
from django.utils.translation import gettext as _


# === STRATEGY SUPPORTING VARIABLES ===
easy_strategies = {
    'naked_pair': 'Naked Pair/Triple',
    'hidden_pair': 'Hidden Pair/Triple'
}
medium_strategies = {}
advanced_strategies = {}
strategies_context = {'easy_strategies': easy_strategies,
                      'medium_strategies': medium_strategies,
                      'advanced_strategies': advanced_strategies}

# === SOLVER SUPPORTING VARIABLES ===
basic_sudokus = {
    'sudoku4x4': 'Sudoku 4x4',
    'sudoku6x6': 'Sudoku 6x6',
    'classic': 'Sudoku 9x9',
    'sudoku16x16': 'Sudoku 16x16'
}
extra_rules = {

}
math_sudokus = {

}
sudokus_context = {'basic_sudokus': basic_sudokus,
                   'extra_rules': extra_rules,
                   'math_sudokus': math_sudokus}

@register.filter
def get_range(val):
    return range(val)

def index(request):
    return render(request, 'index.html')

# ====================================
#           SOLVER VIEWS
# ====================================

def solver_index(request):
    return render(request, 'solver/index.html', sudokus_context)

def solver(request, name):
    template = 'solver/' + name + '.html'
    try:
        django.template.loader.get_template(template)
    except TemplateDoesNotExist:
        raise Http404(_('Aplikace na řešení') + ' "' + name + '" ' + _('nebyla nalezena.'))

    return render(request, template, sudokus_context)

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

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
import django.template.loader
from django.template import TemplateDoesNotExist
from django.utils.translation import gettext as _


easy_strategies = {
    'naked_pair': 'Naked Pair/Triple',
    'hidden_pair': 'Hidden Pair/Triple'
}
medium_strategies = {}
advanced_strategies = {}
strategies_context = {'easy_strategies': easy_strategies,
                      'medium_strategies': medium_strategies,
                      'advanced_strategies': advanced_strategies}


def index(request):
    return render(request, 'index.html')

# ====================================
#           SOLVER VIEWS
# ====================================

def solver_index(request):
    return render(request, 'solver/index.html')

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
        raise Http404(_('Guide') + ' "' + name + '" ' + _('not found.'))

    return render(request, template, strategies_context)

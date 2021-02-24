from django.shortcuts import render
from django.http import HttpResponse

easy_strategies = {
    'naked_pair': 'Naked Pair/Triple',
    'hidden_pair': 'Hidden Pair/Triple'
}
medium_strategies = {}
advanced_strategies = {}
context = {'easy_strategies': easy_strategies,
           'medium_strategies': medium_strategies,
           'advanced_strategies': advanced_strategies}

def index(request):
    return render(request, 'guides/index.html', context)

def detail(request, name):
    template = 'guides/' + name + '.html'
    return render(request, template, context)

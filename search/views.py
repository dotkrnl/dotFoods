from django.shortcuts import render
from django.http import HttpResponseRedirect

from wikipage.models import WikiPage, WikiList, WikiCategory
from search.utils import tokenize

def index(request):
    return render(request, 'search/index.html')

def search_for(request):
    if 'q' not in request.GET:
        return HttpResponseRedirect('/')

    keywords = tokenize(request.GET['q'])
    if not keywords:
        return HttpResponseRedirect('/')

    pages = WikiPage.objects

    selected_lists = []
    # filter out lists if requested
    if 'lists' in request.POST:
        if request.POST.get('lists'):
            selected_lists = request.POST.get('lists').split(',')
            pages = pages.filter(lists__url_name__in=selected_lists)

    selected_categories = []
    # filter out categories if requested
    if 'categories' in request.POST:
        if request.POST.get('categories'):
            selected_categories = request.POST.get('categories').split(',')
            pages = pages.filter(categories__url_name__in=selected_categories)

    # filter out pages that do not match all the keywords
    for keyword in keywords:
        pages = pages.filter(pagekeyword__keyword=keyword)

    # use subquery to calculate the weight of result
    pages = pages.extra(select={
        'weight': 'SELECT SUM(count) ' +
                  'FROM search_pagekeyword ' +
                  'WHERE search_pagekeyword.page_id = ' +
                  'wikipage_wikipage.url_name AND ' +
                  'keyword in %s'},
        select_params=(tuple(keywords),),
    ).order_by('-weight')

    selected_lists_objects = \
        WikiList.objects.filter(url_name__in=selected_lists)
    selected_cates_objects = \
        WikiCategory.objects.filter(url_name__in=selected_categories)

    context = {
        'pages': pages.all(),
        'lists': WikiList.objects.order_by('title').all(),
        'selected_lists': selected_lists_objects,
        'categories': WikiCategory.objects.order_by('title').all(),
        'selected_cates': selected_cates_objects,
        'keyword': request.GET['q'],
    }

    template = 'search/results.html'
    if request.is_ajax():
        template = 'search/results_items.html'

    return render(request, template, context)

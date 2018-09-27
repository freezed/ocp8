from re import search as re_search
from pprint import pformat as pf

from django.shortcuts import render
from django.http import HttpResponse

from . import api

def index(request):
    return render(request, 'ersatz/home.html')

def search(request):

    if not re_search('s=', request.META['QUERY_STRING']):
        data = {
            'satus': False,
            'context': {
                'user_query': request.META['QUERY_STRING'],
            },
        }

    else:
        search = api.SearchProduct(request.GET['s'])
        data = search.result

    return render(request, 'ersatz/result.html', data)

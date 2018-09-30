from re import search as re_search
import urllib.parse as up

from django.shortcuts import render
from . import api


def index(request):
    return render(request, 'ersatz/home.html')


def search(request):
    parts = up.parse_qsl(
        up.urlsplit(request.META['QUERY_STRING'])[3]
    )
    url_qs_parsed = {k:v for (k,v) in parts if k == 's'}

    if not url_qs_parsed:
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

from re import search as re_search
import urllib.parse as up

from django.shortcuts import render
from . import api


def index(request):
    return render(request, 'ersatz/home.html')


def search(request):
    """
    Receives the user request to search a product over OpenFF API

    The context dict() used to render the template is `data` and it's
    formated like this :

    Unvalid :
    {
      'satus': False,
      'context': method path,
      'error': {details/message},
    }

    Valid :
    {
      'satus': True,
      'products': { product dict() },
    }
    """

    parts = up.parse_qsl(request.META['QUERY_STRING'])
    url_qs_parsed = {k:v for (k,v) in parts if k == 's'}

    if not url_qs_parsed:
        data = {
            'satus': False,
            'context': __name__+'.search()',
            'error': {
                'user_query': request.META['QUERY_STRING'],
            },
        }

    else:
        search = api.SearchProduct(request.GET['s'])
        data = search.result

    return render(request, 'ersatz/result.html', data)

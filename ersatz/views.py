import re
from django.shortcuts import render
from pprint import pformat as pf

from django.http import HttpResponse
import requests

from .config import API, FIELD_KEPT

def get_json(url, payload):
    """
    Request API
    """
    try:
        response = requests.get(url, payload)
    except requests.exceptions.ConnectionError as except_detail:
        return {'ConnectionError': pf(except_detail)}

    try:
        api_json = response.json()
        api_json.update({'status': True})
    except Exception as detail:
        return {
            'context': 'get_json() method',
            'error':{'JSONDecodeError': str(detail)}
        }
    else:
        if response.status_code == 200:
            return api_json

        else:
            return {
                'context': 'get_json() method',
                'error':{'status_code': response.status_code}
            }


class SearchProduct:
    """ Class doc """

    def __init__(self, string):
        """ Class initialiser """
        self._url = API['PARAM_SEARCH']
        self._payload = API['PARAM_SEARCH']
        self._payload.update({'search_terms': string})

    def _get_product_dict(self):

        api_response = get_json(API['URL_SEARCH'], self._payload)
        result = api_response

        if api_response['status']:
            products = {}

            for k, p in enumerate(api_response['products']):
                products.update({k: {}})

                for field in FIELD_KEPT['product']:
                    try:
                        products[k].update({field: p[field]})

                    except (TypeError, KeyError) as except_detail:
                        print("Exception: «{}»".format(except_detail))
                        products[k].update({field: False})

            products.update({'context':'response'})
            result = products

        return result

    result = property(_get_product_dict)

def index(request):
    return render(request, 'ersatz/home.html')

def search(request):

    if not re.search('s=', request.META['QUERY_STRING']):
        data = {
            'satus': False,
            'context': {
                'query': request.META['QUERY_STRING'],
            },
        }
        print(data)

    else:
        search = SearchProduct(request.GET['s'])
        data = search.result

    return render(request, 'ersatz/result.html', data)

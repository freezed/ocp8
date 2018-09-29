#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file is part of []() project.

Tools to get data from an API
"""
from sys import exc_info as sys_exc_info
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
            'status': False,
            'error':{'JSONDecodeError': str(detail)}
        }
    else:
        if response.status_code == 200:
            return api_json

        # Hum, how can I have a JSON response with a bad 'status_code'…?
        else:
            return {
                'context': 'get_json() method',
                'status': False,
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

        if api_response['status'] and api_response['count'] > 0:
            products = {'products': []}

            for k, p in enumerate(api_response['products']):
                products['products'].append({})

                for field in FIELD_KEPT['product']:
                    try:
                        products['products'][k].update({field: p[field]})

                    except (TypeError, KeyError) as except_detail:
                        print("{} : «{}»".format(
                            sys_exc_info()[0].__name__,
                            except_detail,
                        ))
                        products['products'][k].update({field: False})

            products.update({
                'context':'response',
                'status': True,
            })
            result = products

        else:
            result = {
                'status': False,
                'context': 'no result'
            }

        return result

    result = property(_get_product_dict)

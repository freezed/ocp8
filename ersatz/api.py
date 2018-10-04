#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file is part of [ocp8](https://github.com/freezed/ocp8) project.

Tools to get data from an API
"""
from pprint import pformat as pf
import requests

from .config import API, FIELD_KEPT


def get_json(url, payload):
    """
    A wrap over `Requests` & `json` library, to centralize API calls

    Returns a dict() :
     - `traceback` if an exception is raised
     - `api_json` if the API calls gets valid response

    The dict() is formated like this :

    Unvalid :
    {
      'status': False,
      'context': method path,
      'error': {details/message},
    }

    Valid :
    {
      'status': True,
      'products': { product dict() },
    }
    """
    traceback = {'context': __name__+'.get_json() method','status': False}

    try:
        response = requests.get(url, payload)
        traceback['error'] = {'url': response.url,'payload': payload}

    except requests.exceptions.ConnectionError as except_detail:
        traceback['error'].update({'ConnectionError': pf(except_detail)})
        return traceback

    try:
        api_json = response.json()
        api_json.update({'status': True})

    except Exception as detail:
        traceback['error'].update({'JSONDecodeError': str(detail)})
        return traceback

    else:
        if response.status_code == 200:
            return api_json

        # How can I have a JSON response with a bad 'status_code'…?
        else:
            traceback['error'].update({'status_code': response.status_code})
            return traceback


class SearchProduct:
    """ Connects to API, get data, purge unused field and format some """

    def __init__(self, string):
        self._payload = API['PARAM_SEARCH']
        self._payload.update({'search_terms': string})
        self._products = []
        self._products_from_api = self._get_products_from_api()

    def _get_products_from_api(self):

        api_response = get_json(API['URL_SEARCH'], self._payload)
        self._products_from_api = api_response

        # API response is valid & non-empty
        if api_response['status'] and api_response['count'] > 0:

            # Iterate on each prod (max 20) and keep only desired fields
            for product in api_response['products']:
                purged_prod = {}
                purged_prod.update(
                    {field: product[field] for field in FIELD_KEPT['product']
                     if field in product}
                )
                purged_prod.update(
                    {field: False for field in FIELD_KEPT['product']
                     if field not in product}
                )
                self._products.append(purged_prod)

            # Parsing is done correctly, add check-fields
            self._products_from_api = {
                'products': self._products,
                'status': True,
            }

        return self._products_from_api

    def _get_result(self):
        return self._products_from_api

    result = property(_get_result)

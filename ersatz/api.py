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
    traceback = {'context': __name__+'.get_json() method', 'status': False}

    try:
        response = requests.get(url, payload)
        traceback['error'] = {'url': response.url, 'payload': payload}

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

    def _get_products_from_api(self):

        api_response = get_json(API['URL_SEARCH'], self._payload)
        json_return = api_response

        # API response is valid & non-empty
        if api_response['status'] and api_response['count'] > 0:
            products = []

            # Iterate on each prod and keep only desired fields
            for product in api_response['products']:
                product_stash = {}
                product_stash.update(
                    {field: product[field] for field in FIELD_KEPT['product']
                     if field in product}
                )
                product_stash.update(
                    {field: False for field in FIELD_KEPT['product']
                     if field not in product}
                )

                product_stash = self.set_categories(product_stash)
                product_stash = self.set_name(product_stash)

                products.append(product_stash)

            # Parsing is done correctly, add check-fields
            json_return = {
                'products': products,
                'status': True,
            }

        return json_return

    result = property(_get_products_from_api)

    @staticmethod
    def set_categories(product_fields):
        """
        Change a `categories_tags` into `categories` list

        Keep all `fr:` tags
        Keep the 2 shortest `en:` tags
        """
        categories_tags = product_fields.pop('categories_tags')
        product_fields.update({"categories": False})

        if categories_tags:
            categories_tags.sort(key=len)
            cat = [tag[3:] for tag in categories_tags if "fr:" in tag]
            cat.extend([tag[3:] for tag in categories_tags if "en:" in tag][:2])

            if len(cat) > 0:
                product_fields.update({"categories": cat})

        return product_fields

    @staticmethod
    def set_name(product_fields):
        """ Concat the `product_name` and the shortest `brands_tags` """
        product_name = product_fields.pop('product_name')
        brands_tags = product_fields.pop('brands_tags')

        if brands_tags:
            brands_tags.sort(key=len)

            name = "{} ({})".format(
                product_name,
                brands_tags[:1][0].capitalize(),
            )

        else:
            name = product_name

        product_fields.update({"name": name})

        return product_fields

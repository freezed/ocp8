#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file is part of [ocp8](https://github.com/freezed/ocp8) project.

A place for Objects & Functions needed in the View of the ersatz module.
All are serving `ersatz.views.views.py`
"""
from pprint import pformat as pf
import urllib.parse as up

import requests

from django.contrib.auth.models import User

from ersatz.models import Favorite, Product, Category
from ersatz.config import API, PRODUCT_FIELD, SPECIAL_PRODUCT_FIELD,VIEWS_MSG_NO_FAV


def get_search_context(request):
    """
    Receives the user request to search a product over OpenFF API

    The context dict() used to render the template is `data` and it's
    formated like this :

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

    parts = up.parse_qsl(request.META['QUERY_STRING'])
    # Get QS from omega/searchform.html, waiting for `s=search_terms`
    url_qs_parsed = {'search_terms':v for (k,v) in parts if k == 's'}

    if not url_qs_parsed:
        data = {
            'status': False,
            'context': __name__+'.get_search_context()',
            'error': API['EMPTY'],
        }

    else:
        try:
            # Get QS from ersatz/list.html, waiting for `p=int(page_number)`
            url_qs_parsed.update({'page': int(v) for (k,v) in parts if k == 'p'})
        except ValueError as except_detail:
            print("ValueError in URL : 'p={}' [{}]".format(
                request.GET['p'],
                except_detail,
            ))

        search = SearchProduct(url_qs_parsed)
        data = search.result

    return data


def update_db(data):
    """ Update DB with products loaded in the search view """

    # list all distinct categories
    categories_set = {
        categories
        for product in data['products']
        if product['categories'] is not False
        for categories in product['categories']
    }

    # drop existing categories
    new_categories = (
        cat
        for cat in categories_set
        if not Category.objects.filter(name=cat).exists()
    )

    # create category
    for category in new_categories:
        Category.objects.create(name=category)

    # drop products already in DB
    new_products = (
        prod
        for prod in data['products']
        if not Product.objects.filter(code=prod['code']).exists()
    )

    # add products & associated cat in DB
    for product in new_products:

        # Set False fields w/ an empty string
        product.update(
            {field: '' for field in product if product[field] is False}
        )

        # Remove temporary special fields, see config for details
        field_dict = {
            field: product[field][:255]  # TODO : word based splitting
            for field in PRODUCT_FIELD
            if field not in SPECIAL_PRODUCT_FIELD
        }

        product_candidate = Product.objects.create(**field_dict)

        # Associate categories to products
        product_cat = (
            (name, Category.objects.get(name=name))
            for name in product['categories']
            if product['categories'] is not False
        )

        for cat in product_cat:
            product_candidate.category.add(cat[1])


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
    # TODO : Find a way to export try/except statement to improve readability
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


def list_favorite(request_user_id):
    """
    Get user's favorites in a dict like this :
    """

    context = {
        'status': True,
        'favorites': Favorite.objects.filter(users_id=request_user_id)
    }

    if context['favorites'].count() == 0:
        context.update({'message': VIEWS_MSG_NO_FAV})

    return context


def save_favorite(request_user_id, e_code, p_code):
    """
    Create a favorite table

    A favorite is a product, a substitute asciated w/ a user

    :param int request_user_id: User id
    :param int e_code: substitute product code (EAN 13)
    :param int p_code: product product code (EAN 13)
    """

    # TODO : request DB once by models
    context = {
        'status': True,
        'product': Product.objects.values().get(code=p_code),
        'substitute': Product.objects.values().get(code=e_code),
        'message': 'Ce substitut était déjà associé à ce produit'
    }

    # Get or Create favorite
    favorite, created = Favorite.objects.get_or_create(
        users=User.objects.get(id=request_user_id),
        products=Product.objects.get(code=p_code),
        substitutes=Product.objects.get(code=e_code),
    )

    if created:
        context.update({'message': 'Substitut enregistré'})

    return context


class SearchProduct:
    """ Connects to API, get data, purge unused field and format some """

    def __init__(self, url_qs_parsed):
        self._payload = url_qs_parsed
        self._payload.update(**API['PARAM_SEARCH'])

    def _get_products_from_api(self):

        api_response = get_json(API['URL_SEARCH'], self._payload)
        json_return = api_response

        # API response is valid & non-empty
        if api_response['status'] and api_response['count'] > 0:
            products = []
            pagination = self.get_pagination(
                api_response['count'],
                api_response['page'],
                api_response['page_size'],
            )

            # Iterate on each prod and keep only desired fields
            for product in api_response['products']:
                product_stash = {}
                product_stash.update(
                    {field: product[field] for field in PRODUCT_FIELD
                     if field in product}
                )
                product_stash.update(
                    {field: False for field in PRODUCT_FIELD
                     if field not in product}
                )

                product_stash = self.set_categories(product_stash)
                product_stash = self.set_name(product_stash)

                products.append(product_stash)

            # Parsing is done correctly, add check-fields
            json_return = {
                'products': products,
                'status': True,
                'pagination': pagination,
            }

        # Response without products
        elif api_response['status'] and api_response['count'] == 0:
            json_return.update({
                'status': False,
                'context': __name__+'._get_products_from_api()',
                'error': API['NO_PROD'].format(
                    self._payload['search_terms']
            )})

        return json_return

    result = property(_get_products_from_api)

    def get_pagination(self, count, page, page_size):
        # sometime API response gives number in a string :-/
        count = int(count)
        page = int(page)
        page_size = int(page_size)
        pagination = {
            'page': page,
            'url_query': '?s={}'.format(self._payload['search_terms']),
        }

        # Pages number calculation
        last = count // page_size

        if count % page_size > 0:
            last += 1

        pagination.update({'last': last})

        # Contextual framing
        if page == 0:
            pagination.update({'following': 2})

        elif page >= last:
            pagination.update({'previous': last - 1})

        else:
            pagination.update({'previous': page - 1})
            pagination.update({'following': page + 1})

        return pagination

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


class ErsatzProduct:
    """ User choose a product, this object processes substitution """

    def __init__(self, product_code):
        """ Class initialiser """
        self.product = Product.objects.get(code=int(product_code))
        self.product_val = Product.objects.values().get(code=int(product_code))

    def get_substitute_context(self):
        """
            Return will be used as a templates context.
            Return is JSON formated :

                - if a substitutes product candidate list is found

                    context = {
                        'status': True,
                        'product': {},
                        'candidate': [],
                        'slist': [],
                        'count': '',
                    }

                - if no candidate is found

                    context = {
                        'status': False,
                        'message': '',
                    }
        """

        context = {
            'status':False,
            'message': 'Le nutriscore est déjà «A»',
        }

        if self.product_val['nutrition_grades'] != 'a':
            context = self.get_candidate(self.product_val['nutrition_grades'])

        context.update({'product': self.product_val})

        return context

    def get_candidate(self, png):
        context = {
            'candidate':[],
            'status': False,
            'message': 'Pas de substitut trouvé',
        }

        # data structure depending on png (aka product['nutrition_grades'])
        ng_sequence = {
            'b': ['a'],
            'c': ['a', 'b'],
            'd': ['a', 'b', 'c'],
            'e': ['a', 'b', 'c', 'd'],
        }
        ersatz_candidates = {cat: list() for cat in ng_sequence[png]}
        summary_nutri = {cat: list() for cat in ng_sequence[png]}

        # get product categories
        product_cat = Category.objects.values_list('id', flat=True).filter(products=self.product)

        # Collect each candidates_id in same cat w/ better nutrition_grades
        for nutri in ersatz_candidates:
            ersatz_candidates[nutri].extend([product_candidate for c in product_cat for product_candidate in Product.objects.values_list('id', flat=True).filter(category=c, nutrition_grades=nutri)])

            # Count candidates_id occurrences across all categories
            summary_nutri[nutri].extend([(product, ersatz_candidates[nutri].count(product)) for product in set(ersatz_candidates[nutri])])

            # Sort candidates_id max occurrences 1st & keep only candidates_id occurences gt 2
            context['candidate'].extend([cand_id for cand_id, occur in sorted(summary_nutri[nutri], reverse=True, key=lambda sum_n: sum_n[1]) if occur > 1][:3])

        # Data return
        count = len(context['candidate'])

        if count > 0:
            context.update({'slist': list(
                Product.objects.values().filter(
                    id__in=context['candidate']
                ).order_by('nutrition_grades')
            )})
            context['status'] = True
            context['count'] = count

        return context

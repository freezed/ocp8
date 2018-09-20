#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file is part of [ocp8](https://github.com/freezed/ocp8) project.
"""

APP = {
    'NAME':'ersatz',
    'DESC':'Trouver un substitut',
}

API = {
    'URL_SEARCH':'https://fr.openfoodfacts.org/cgi/search.pl',
    # 'URL_CATEGO':'',
    # 'URL_PRODUC':'',
    # '':'',
    'PARAM_SEARCH': {
        'search_terms': '',
        'search_simple': 1,
        'action': 'process',
        'json': 1,
    },
    # 'PARAM_CATEGO': {
        # '': '',
        # '': '',
    # },
    # 'PARAM_PRODUC': {
        # '': '',
        # '': '',
    # },
}
FIELD_KEPT = {
    'product': [
        'product_name',
        'nutrition_grades',
        'categories_tags',
        'code',
    ],
}

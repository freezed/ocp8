"""
This file is part of [ocp8](https://github.com/freezed/ocp8) project.
"""

APP = {
    'NAME':'ersatz',
    'DESC':'Trouver un substitut',
}

API = {
    'URL_SEARCH':'https://fr.openfoodfacts.org/cgi/search.pl',
    'PARAM_SEARCH': {
        'search_simple': 1,
        'action': 'process',
        'json': 1,
    },
    'NO_PROD': 'OpenFoodFacts ne donne pas de produits pour la requête : «{}»',
}

FIELD_KEPT = {
    'product': [
        'product_name',
        'brands_tags',
        'nutrition_grades',
        'categories_tags',
        'nova_group',
        'code',
    ],
}

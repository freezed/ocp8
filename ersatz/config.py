"""
This file is part of [ocp8](https://github.com/freezed/ocp8) project.
"""
from ersatz.models import Product

API = {
    'URL_SEARCH':'https://fr.openfoodfacts.org/cgi/search.pl',
    'PARAM_SEARCH': {
        'search_simple': 1,
        'action': 'process',
        'json': 1,
    },
    'NO_PROD': 'OpenFoodFacts ne donne pas de produits pour la requête : «{}»',
}

# Using ersatz.models.Products attributes to get fields from API.
PRODUCT_FIELD = [
    attrib
    for attrib in vars(Product)
    if not attrib.startswith(('_', 'favorites_'))
    if not attrib in ['objects', 'id', 'category']
    and not callable(getattr(Product, attrib))
]

# Special field : needed to get API data, but processed/renamed/deleted before
# storage in DB. Beware choosing news names not used in original API data.
# See @staticmethod in ersatz.view.api.SearchProduct to process this fields
SPECIAL_PRODUCT_FIELD = ['categories_tags','product_name','brands_tags']

PRODUCT_FIELD.extend(SPECIAL_PRODUCT_FIELD)

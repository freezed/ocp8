"""
This file is part of [ocp8](https://github.com/freezed/ocp8) project.
"""
from ersatz.models import Product

API = {
    'URL_SEARCH':'https://fr.openfoodfacts.org/cgi/search.pl',
    'URL_PRODUCT':'https://fr.openfoodfacts.org/api/v0/product/{}.json',
    'PARAM_SEARCH': {
        'search_simple': 1,
        'action': 'process',
        'json': 1,
    },
    'NO_PROD': 'OpenFoodFacts ne donne pas de produits pour la recherche : «{}»',
    'EMPTY': 'Bizarrement OpenFoodFacts ne donne pas de produits pour une recherche vide…',
}

# Using ersatz.models.Product attributes to get fields from API.
# Using ersatz.tests.test_comands.test_get_db_products
BASE_PRODUCT_FIELD = [
    attrib
    for attrib in vars(Product)
    if not attrib.startswith(('_', 'favorites_'))
    if not attrib in ['objects', 'id', 'category']
    and not callable(getattr(Product, attrib))
]

# Special field : needed to get API data, but processed/renamed/deleted before
# storage in DB. Beware choosing news names not used in original API data.
# See @staticmethod in ersatz.view.toolbox.SearchProduct to process this fields
SPECIAL_PRODUCT_FIELD = ['categories_tags','product_name','brands_tags']

PRODUCT_FIELD = list(BASE_PRODUCT_FIELD)
PRODUCT_FIELD.extend(SPECIAL_PRODUCT_FIELD)

VIEWS_MSG_NO_FAV = "Vous n'avez pas encore enregistré de favoris, il est temps de faire une petite recherche!"
VIEWS_MSG_LOGIN = 'Vous devez être connecté pour utiliser cette fonctionnalité'
VIEWS_MSG_CANDIDATE_BEST = "Le nutriscore est déjà «A»"
VIEWS_MSG_CANDIDATE_NONE = "Pas de substitut trouvé"
VIEWS_ERR = "Oups… «{}»"

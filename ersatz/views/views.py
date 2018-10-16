from re import search as re_search
import urllib.parse as up

from django.shortcuts import render
from ersatz.models import Category, Product
from . import api

def _get_search_context(request):
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
    url_qs_parsed = {'search_terms':v for (k,v) in parts if k == 's'}

    if not url_qs_parsed:
        data = {
            'status': False,
            'context': __name__+'.search()',
            'error': {
                'user_query': request.META['QUERY_STRING'],
            },
        }

    else:
        try:
            url_qs_parsed.update({'page': int(v) for (k,v) in parts if k == 'p'})
        except ValueError as except_detail:
            print("ValueError in URL : 'p={}' [{}]".format(
                request.GET['p'],
                except_detail,
            ))

        search = api.SearchProduct(url_qs_parsed)
        data = search.result

    return data


def _update_db(data):
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

    # #### # DEVLOG # #####
    false_field = dict()
    # #### # DEVLOG # #####

    # add products in DB
    for product in new_products:
        # #### # DEVLOG # #####
        false_field.update({product['name']: field for field in product if product[field] is False})
        # #### # DEVLOG # #####

        product.update(
            {field: '' for field in product if product[field] is False}
        )
        product_candidate = Product.objects.create(
            name=product['name'],
            nutrition_grades=product['nutrition_grades'],
            nova_group=product['nova_group'],
            code=product['code'],
        )

        product_cat = (
            (name, Category.objects.get(name=name))
            for name in product['categories']
            if product['categories'] is not False
        )

        for cat in product_cat:
            product_candidate.category.add(cat[1])

    # #### # DEVLOG # #####
    print('fields emptied : {}'.format(false_field))
    # #### # DEVLOG # #####

def index(request):
    return render(request, 'ersatz/home.html')


def search(request):
    data = _get_search_context(request)

    # if status == True : there is some stuff to store in DB
    if data['status']:
        _update_db(data)

    return render(request, 'ersatz/result.html', data)

def product(request, code):
    ersatz = api.ErsatzProduct(code)
    candidates = ersatz.get_candidates()

    if candidates['status']:
        template = 'ersatz/candidates.html'

    else:
        template = 'ersatz/no-candidates.html'

    return render(request, template, candidates)

def favorite(request, e_code, p_code):
    return render(request, 'ersatz/favorite.html', {
        'e_code': e_code, 'p_code': p_code
    })

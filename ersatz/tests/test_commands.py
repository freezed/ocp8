from pytest import fixture, mark
import json

from ersatz.management.commands.prodsync import Command
from ersatz.models import Product

@fixture
def fill_20():
    """ get 20 products to populate DB """

    with open("ersatz/tests/samples/processed-fromage-page_1.json", "r") as json_file:
        PRODUCTS = json.load(json_file)['products']

    for prod in PRODUCTS:
        del(prod['categories'])
        prod['ingredients_text'] = prod['ingredients_text'][:255]

        if not prod['nutrition_grades']:
            prod['nutrition_grades'] = ''

        if not prod['image_front_thumb_url']:
            prod['image_front_thumb_url'] = ''

        Product.objects.create(**prod)

@mark.parametrize("idx,label,value",[
    (0,'code','3073780258098'),
    (19,'code','3222110023961'),
    (0,'nutrition_grades','d'),
    (19,'nutrition_grades','d'),
])
@mark.django_db
def test_get_db_products(fill_20, idx, label, value):
    """ test a DB request to get products  """

    cmd_instance = Command()
    prods = cmd_instance.dbproducts()

    assert prods[idx][label] == value


""" for a product request api """


""" for an api response check if is differant than DB data """


""" update product in DB """


""" print updates summary """

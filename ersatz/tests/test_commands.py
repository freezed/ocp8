import json

from pytest import fixture, mark

from ersatz.management.commands.prodsync import Command
from ersatz.models import Product
from ersatz.config import BASE_PRODUCT_FIELD


# ##############################################################################
#   ersatz.management.commands.prodsync
# ##############################################################################

class FakeRequestsProduct:
    """ get_json() mock class """

    samples = {
        "changed": "ersatz/tests/samples/api-faisselle-short-changed.json",
        "populate": "ersatz/tests/samples/processed-fromage-page_1.json",
    }

    def __init__(self, context):
        self.sample = self.samples[context]

    def get_json(self, url):
        with open(self.sample, "r") as json_file:
            json_response_from_api = json.load(json_file)
        return json_response_from_api


@fixture
def db20prod():
    """ get 20 products to populate DB """

    PRODUCTS = FakeRequestsProduct('populate').get_json('url')['products']

    for prod in PRODUCTS:
        del prod['categories']
        prod['ingredients_text'] = prod['ingredients_text'][:255]

        if not prod['nutrition_grades']:
            prod['nutrition_grades'] = ''

        if not prod['image_front_thumb_url']:
            prod['image_front_thumb_url'] = ''

        Product.objects.create(**prod)

    return Command()


@fixture
def api_faisselle_changed():
    """ Mock API response for changed product Faisselle (code=3184670001080) """
    return FakeRequestsProduct('changed').get_json('url')['products']



# ##############################################################################
@mark.parametrize("idx,label,value", [
    (0, 'code', '3073780258098'),
    (19, 'code', '3222110023961'),
    (0, 'nutrition_grades', 'd'),
    (19, 'nutrition_grades', 'd'),
])
@mark.django_db
def test_get_db_products(db20prod, idx, label, value):
    """ test a DB request to get products  """

    prods = db20prod.products

    assert prods[idx][label] == value

    for p in prods:
        assert set(BASE_PRODUCT_FIELD).issubset(p.keys())


# ##############################################################################
def mock_get_json_from_api_valid_changed(url):
    """ get_json() mock function """
    return FakeRequestsProduct('changed').get_json('url')


@mark.parametrize("label", [
    ("image_front_thumb_url"),
    ("image_front_url"),
    ("image_nutrition_url"),
    ("ingredients_text"),
])
@mark.django_db
def test_compare_changed_product(db20prod, api_faisselle_changed, label, monkeypatch):
    """ test when a products is changed on OFF """
    monkeypatch.setattr(
        'ersatz.management.commands.prodsync.get_json',
        mock_get_json_from_api_valid_changed
    )
    changes = db20prod.changes(api_faisselle_changed['code'])

    for field in changes.keys():
        assert field in BASE_PRODUCT_FIELD
    assert changes[label] == api_faisselle_changed[label]


@mark.django_db
def test_compare_unchanged_product(db20prod):
    """ test when a products is unchanged on OFF """
    pass

""" update product in DB """


""" print updates summary """

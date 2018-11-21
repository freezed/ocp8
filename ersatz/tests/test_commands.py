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
        "unchanged": "ersatz/tests/samples/api-faisselle-short-unchanged.json",
        "changed": "ersatz/tests/samples/api-faisselle-short-changed.json",
        "changes": "ersatz/tests/samples/faisselle-changes.json",
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


@fixture
def api_faisselle_unchanged():
    """ Mock API response for unchanged product Faisselle (code=3184670001080) """
    return FakeRequestsProduct('unchanged').get_json('url')['products']


@fixture
def faisselle_changes():
    """ Mock API response for unchanged product Faisselle (code=3184670001080) """
    return FakeRequestsProduct('changes').get_json('url')['products']



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


# ##############################################################################
def mock_get_json_from_api_valid_unchanged(url):
    """ get_json() mock function """
    return FakeRequestsProduct('unchanged').get_json('url')


@mark.django_db
def test_compare_unchanged_product(db20prod, api_faisselle_unchanged, monkeypatch):
    """ test when a products is unchanged on OFF """
    monkeypatch.setattr(
        'ersatz.management.commands.prodsync.get_json',
        mock_get_json_from_api_valid_unchanged
    )
    changes = db20prod.changes(api_faisselle_unchanged['code'])

    assert changes == {}


@mark.parametrize("field", [
    ("image_front_thumb_url"),
    ("image_front_url"),
    ("image_nutrition_url"),
    ("ingredients_text"),
])
@mark.django_db
def test_dbupdate_changes_in_db(db20prod, faisselle_changes, field, monkeypatch):
    """ Test if somes changes on a product have been updated in DB """
    monkeypatch.setattr(
        "ersatz.management.commands.prodsync.Command.changes",
        mock_get_json_from_api_valid_changed
    )
    db20prod.dbupdate(faisselle_changes)
    db_prod = {
        key: val for key, val in Product.objects.values().filter(
            code=faisselle_changes['code']
        )[0].items()
    }

    assert faisselle_changes[field] == db_prod[field]

import os
import json
import urllib.parse as up

import pytest

from django.db.models import Count

from ersatz.config import API, PRODUCT_FIELD
from ersatz.models import Product, Category
from ersatz.views import toolbox as toolbox
from ersatz.views import views as views


################################################################################
#   ersatz.views.toolbox.get_search_context()
################################################################################

# For a invalid user request, app returns a JSON standardised error
class FakeUserRequestGet:
    def __init__(self, QUERY_STRING):
        parts = up.parse_qsl(QUERY_STRING)

        self.META = {'QUERY_STRING': QUERY_STRING}
        self.GET = {parts[0][0]: parts[0][1]}

def test_user_request_invalid():
    request = FakeUserRequestGet("foobars=This string doesn't matter test is about unvalid request key (here : 'foobars')")
    response = toolbox.get_search_context(request)
    assert response == {
        'context': 'ersatz.views.toolbox.get_search_context()',
        'error': API['EMPTY'],
        'status': False
    }

# For an valid user request, app returns a JSON standardised response
class FakeSearchProductValid:
    """ ersatz.views.toolbox.SearchPoduct mock class """
    result = {'status': True, 'foo': 'bar'}

def mock_user_request_valid(query):
    """ ersatz.views.toolbox.SearchPoduct mock function """
    return FakeSearchProductValid

def test_user_request_valid(monkeypatch):
    monkeypatch.setattr('ersatz.views.toolbox.SearchProduct', mock_user_request_valid)
    request = FakeUserRequestGet('s=ValidUserInput')
    output_witness = FakeSearchProductValid.result
    output_processed = toolbox.get_search_context(request)
    assert output_processed == output_witness
################################################################################


################################################################################
#   ersatz.views.toolbox.update_db()
################################################################################

@pytest.mark.django_db
def test_update_db():
    with open("ersatz/tests/samples/processed-fromage-page_1.json", "r") as json_file:
        input_sample = json.load(json_file)

    CAT_WITNESS = [
        ('dairies', 17), ('cheeses', 12), ('spreads', 5), ('gouter', 3)
    ]

    toolbox.update_db(input_sample)
    cat_resume = Category.objects.annotate(
        prod_count=Count('products')
    ).values('name', 'prod_count').order_by('-prod_count')[:4]

    cat_processed = [(cat['name'],cat['prod_count']) for cat in cat_resume]

    assert Product.objects.count() == 20
    assert Category.objects.count() == 22
    assert cat_processed == CAT_WITNESS
################################################################################


################################################################################
#   ersatz.views.toolbox.requests()
################################################################################

# Test API data processing
class FakeRequestsJSONValid:
    """ Requests.reponse mock class """
    status_code = 200
    url = 'test_url'

    def json():
        return {'foo': 'bar'}

def mock_requests_get_valid(url, payload):
    """ Requests.get() mock function """
    return FakeRequestsJSONValid

def test_get_json_valid(monkeypatch):
    monkeypatch.setattr('ersatz.views.toolbox.requests.get', mock_requests_get_valid)
    response = toolbox.get_json('url', 'payload')
    assert response['status']
    assert response['foo'] == 'bar'


class FakeRequestsJSONInvalid:
    """ Requests.reponse mock class"""
    status_code = 'foobar'
    url = 'test_url'

def mock_requests_get_json_invalid(url, payload):
    """ Requests.get() mock function """
    return FakeRequestsJSONInvalid

def test_get_json_json_invalid(monkeypatch):
    monkeypatch.setattr('ersatz.views.toolbox.requests.get', mock_requests_get_json_invalid)
    response = toolbox.get_json('url', 'payload')
    assert 'get_json()' in response['context']
    assert 'JSONDecodeError' in response['error']
    assert not response['status']


class FakeRequestsStatusCodeInvalid:
    """ Requests.reponse mock class"""
    status_code = 'foobar'
    url = 'test_url'


    def json():
        return {'foo': 'bar'}

def mock_requests_get_status_code_invalid(url, payload):
    """ Requests.get() mock function """
    return FakeRequestsStatusCodeInvalid

def test_get_json_status_code_invalid(monkeypatch):
    monkeypatch.setattr('ersatz.views.toolbox.requests.get', mock_requests_get_status_code_invalid)
    response = toolbox.get_json('url', 'payload')
    assert 'get_json()' in response['context']
    assert response['error']['status_code'] == 'foobar'
    assert not response['status']
################################################################################


################################################################################
#   ersatz.views.toolbox.SearchProduct.result
################################################################################

# For products returned by API :
# - Products are not all the same after processing (non-regression issue #19)
# - All fields/values expected are here
class FakeGetJsonFromApiValid:
    """ get_json() mock class """
    def get_json(url, payload):
        with open("ersatz/tests/samples/api-fromage-page_1.json", "r") as json_file:
            json_response_from_api = json.load(json_file)
        return json_response_from_api

def fake_get_json_from_api_valid(url, payload):
    """ get_json() mock function """
    return FakeGetJsonFromApiValid.get_json('url', 'payload')

def test_search_product_valid(monkeypatch):
    with open("ersatz/tests/samples/processed-fromage-page_1.json", "r") as json_file:
        output_sample = json.load(json_file)

    monkeypatch.setattr('ersatz.views.toolbox.get_json', fake_get_json_from_api_valid)
    output_processed = toolbox.SearchProduct({'search_terms': 'string'})
    assert output_processed.result['products'] == output_sample['products']

# API response is not valid, and return a `satus` == False
def fake_get_json_from_api_invalid(url, payload):
    """ ersatz.views.toolbox.get_json fake function """
    return {'status': False}

def test_search_product_invalid(monkeypatch):
    monkeypatch.setattr('ersatz.views.toolbox.get_json', fake_get_json_from_api_invalid)
    output_processed = toolbox.SearchProduct({'query': 'string'})
    assert not output_processed.result['status']
################################################################################


################################################################################
#   ersatz.views.toolbox.SearchProduct.__init__
################################################################################

# Non-regresion test for issue #20 :
# - API params in configuration were overriden after each search
def test_search_product__init__():
    query_set_1 = {'search_terms': 'foo','foobar': 1664}
    query_set_2 = {'search_terms': 'bar'}

    witness = dict()
    witness.update(**query_set_2)
    witness.update(**API['PARAM_SEARCH'])

    search_1 = toolbox.SearchProduct(query_set_1)
    search_2 = toolbox.SearchProduct(query_set_2)

    assert witness == search_2._payload
################################################################################


################################################################################
#   ersatz.views.toolbox.ErsatzProduct
################################################################################
@pytest.mark.django_db
class TestErsatzProduct:
    with open("ersatz/tests/samples/processed-fromage-page_1.json", "r") as json_file:
        input_sample = json.load(json_file)

    toolbox.update_db(input_sample)

    def test_ersatz_product__init__(self):
        # test_ep = toolbox.ErsatzProduct(3073780258098)
        # assert test_ep.product.id == 3073780258098
        pass

    def test_ersatz_product_get_substitute_context(self):
        pass

    def test_ersatz_product_get_candidate(self):
        pass

    # def test_ersatz_product_():

################################################################################

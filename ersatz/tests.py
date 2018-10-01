import os
import json
import urllib.parse as up
from . import api, views
from .config import FIELD_KEPT


#########
# VIEWS #
#########
class FakeGetRequest:
    def __init__(self, QUERY_STRING):
        parts = up.parse_qsl(up.urlsplit(QUERY_STRING)[3])

        self.META = {'QUERY_STRING': QUERY_STRING}
        self.GET = {parts[0][0]: parts[0][1]}


def test_invalid_request():
    request = FakeGetRequest('?foos=bar')
    response = views.search(request)
    assert b'Status : False' in response.content


class FakeSearchProductValid:
    """ ersatz.api.SearchPoduct mock class """
    result = {'status': True}


def mock_search_product_valid(query):
    """ ersatz.api.SearchPoduct mock function """
    return FakeSearchProductValid


def test_valid_request(monkeypatch):
    monkeypatch.setattr('ersatz.api.SearchProduct', mock_search_product_valid)
    request = FakeGetRequest('?s=sel')
    response = views.search(request)
    assert b'Status : True' in response.content

#########
#  API  #
#########
def fake_get_json_valid(url, payload):
    """ ersatz.api.get_json fake function """
    return {
        'count': 2,
        'status': True,
        'page': 1,
        'skip': 0,
        'page_size': '2',
        'products': [
            {
                'product_name': 'Foo',
                'nutrition_grades': 'c',
                'categories_tags': [
                    'en:fresh-foods',
                    'en:dairies',
                    'fr:fromages-blancs',
                ],
                'code': 1664,
                "_keywords": [],
                "packaging_tags": [
                    "carton",
                    "sachet-plastique"
                ],
                "ingredients_n_tags": [],
                "countries_beforescanbot": "France",
                "languages": {
                    "en:french": 6
                },
            },
            {
                'product_name': 'ooF',
                'nutrition_grades': 'b',
                'categories_tags': [
                    'en:fermented-foods',
                    'en:fermented-milk-products',
                    'fr:fromage-a-pate-pressee',
                    'fr:picodon',
                ],
                'code': 4661,
                "_keywords": [],
                "packaging_tags": [
                    "PET",
                    "papier"
                ],
                "ingredients_n_tags": [],
                "countries_beforescanbot": "France",
                "languages": {
                    "en:french": 6
                },
            },
        ]
    }


def test_search_product_valid(monkeypatch):
    monkeypatch.setattr('ersatz.api.get_json', fake_get_json_valid)
    test_search = api.SearchProduct('valid_query_string')
    product_count = len(test_search.result['products'])
    api_json = fake_get_json_valid('url', {'foo': 'bar'})

    # Test JSON response keys
    for field in ('status', 'context', 'products'):
        assert field in test_search.result

    # Test fields of first product
    for field in FIELD_KEPT['product']:
        assert field in test_search.result['products'][0]

    # Test product quantity
    assert product_count == api_json['count']


def fake_get_json_invalid(url, payload):
    """ ersatz.api.get_json fake function """
    return {'status': False}


def test_search_product_invalid(monkeypatch):
    monkeypatch.setattr('ersatz.api.get_json', fake_get_json_invalid)
    test_search = api.SearchProduct('fake_string')
    assert not test_search.result['status']


class FakeRequestsJSONValid:
    """ Requests.reponse mock class """
    status_code = 200

    def json():
        return {'foo': 'bar'}


def mock_requests_get_valid(url, payload):
    """ Requests.get() mock function """
    return FakeRequestsJSONValid


def test_get_json_valid(monkeypatch):
    monkeypatch.setattr('ersatz.api.requests.get', mock_requests_get_valid)
    response = api.get_json('url', 'payload')
    assert response['status']
    assert response['foo'] == 'bar'


class FakeRequestsJSONInvalid:
    """ Requests.reponse mock class"""
    status_code = 'foobar'


def mock_requests_get_json_invalid(url, payload):
    """ Requests.get() mock function """
    return FakeRequestsJSONInvalid


def test_get_json_json_invalid(monkeypatch):
    monkeypatch.setattr('ersatz.api.requests.get', mock_requests_get_json_invalid)
    response = api.get_json('url', 'payload')
    assert response['context'] == 'get_json() method'
    assert 'JSONDecodeError' in response['error']
    assert not response['status']


class FakeRequestsStatusCodeInvalid:
    """ Requests.reponse mock class"""
    status_code = 'foobar'

    def json():
        return {'foo': 'bar'}


def mock_requests_get_status_code_invalid(url, payload):
    """ Requests.get() mock function """
    return FakeRequestsStatusCodeInvalid


def test_get_json_status_code_invalid(monkeypatch):
    monkeypatch.setattr('ersatz.api.requests.get', mock_requests_get_status_code_invalid)
    response = api.get_json('url', 'payload')
    assert response['context'] == 'get_json() method'
    assert response['error']['status_code'] == 'foobar'
    assert not response['status']

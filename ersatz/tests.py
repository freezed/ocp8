import urllib.parse as up
import pytest
from . import api, views
from .config import FIELD_KEPT

###########
## VIEWS ##
###########
class FakeGetRequest:
    def __init__(self, QUERY_STRING):
        parts = up.parse_qsl(up.urlsplit(QUERY_STRING)[3])

        self.META = {'QUERY_STRING': QUERY_STRING}
        self.GET = {parts[0][0]: parts[0][1]}

def test_invalid_request():
    request = FakeGetRequest('?q=foobar')
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

###########
##  API  ##
###########
def fake_get_json_valid(url, payload):
    """ ersatz.api.get_json fake function """
    return {
        'count': 1,
        'status': True,
        'page': 1,
        'skip': 0,
        'page_size': '1',
        'products': [
            {
                'product_name': 'Foo',
                'nutrition_grades': 'c',
                # no 'categories_tags' to test missing field feature
                'code': 1664,
            },
        ]
    }

def test_search_product_valid(monkeypatch):
    monkeypatch.setattr('ersatz.api.get_json', fake_get_json_valid)
    test_search = api.SearchProduct('fake_string')
    product_count = len(test_search.result['products'])
    api_json = fake_get_json_valid('url', {'foo': 'bar'})

    # Test JSON response keys
    for field in ('status','context','products'):
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

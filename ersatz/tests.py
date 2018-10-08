import os
import json
import urllib.parse as up
from . import api, views
from .config import FIELD_KEPT

################################################################################
#   ersatz.views._get_search_context()
################################################################################

# For a invalid user request, app returns a JSON standardised error
class FakeUserRequestGet:
    def __init__(self, QUERY_STRING):
        parts = up.parse_qsl(QUERY_STRING)

        self.META = {'QUERY_STRING': QUERY_STRING}
        self.GET = {parts[0][0]: parts[0][1]}

def test_user_request_invalid():
    request = FakeUserRequestGet("foobars=This string doesn't matter test is about unvalid request key (here : 'foobars')")
    response = views._get_search_context(request)
    assert response == {
        'context': 'ersatz.views.search()',
        'error': {'user_query': "foobars=This string doesn't matter test is about unvalid request key (here : 'foobars')"},
        'status': False
    }

# For an valid user request, app returns a JSON standardised response
class FakeSearchProductValid:
    """ ersatz.api.SearchPoduct mock class """
    result = {'status': True, 'foo': 'bar'}

def mock_user_request_valid(query):
    """ ersatz.api.SearchPoduct mock function """
    return FakeSearchProductValid

def test_user_request_valid(monkeypatch):
    monkeypatch.setattr('ersatz.api.SearchProduct', mock_user_request_valid)
    request = FakeUserRequestGet('s=ValidUserInput')
    output_witness = FakeSearchProductValid.result
    output_processed = views._get_search_context(request)
    assert output_processed == output_witness
################################################################################

#########
#  API  #
#########
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
    monkeypatch.setattr('ersatz.api.requests.get', mock_requests_get_valid)
    response = api.get_json('url', 'payload')
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
    monkeypatch.setattr('ersatz.api.requests.get', mock_requests_get_json_invalid)
    response = api.get_json('url', 'payload')
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
    monkeypatch.setattr('ersatz.api.requests.get', mock_requests_get_status_code_invalid)
    response = api.get_json('url', 'payload')
    assert 'get_json()' in response['context']
    assert response['error']['status_code'] == 'foobar'
    assert not response['status']


################################################################################
#   ersatz.api.SearchProduct.result
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

    monkeypatch.setattr('ersatz.api.get_json', fake_get_json_from_api_valid)
    output_processed = api.SearchProduct({'search_terms': 'string'})
    assert output_processed.result['products'] == output_sample['products']

# API response is not valid, and return a `satus` == False
def fake_get_json_from_api_invalid(url, payload):
    """ ersatz.api.get_json fake function """
    return {'status': False}

def test_search_product_invalid(monkeypatch):
    monkeypatch.setattr('ersatz.api.get_json', fake_get_json_from_api_invalid)
    output_processed = api.SearchProduct({'query': 'string'})
    assert not output_processed.result['status']
################################################################################

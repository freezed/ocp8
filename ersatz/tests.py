import urllib.parse as up
import pytest
from . import views

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

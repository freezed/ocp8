import pytest
from . import views

###########
## VIEWS ##
###########
class InvalidRequest:
    META = {'QUERY_STRING': '?foo=bar&q=foobar'}

def test_invalid_request():
    request = InvalidRequest()
    response = views.search(request)
    assert b'Status : False' in response.content

class ValidRequest:
    META = {'QUERY_STRING': '?foo=bar&s=sel'}
    GET = {'s': 'sel'}

def test_valid_request():
    request = ValidRequest()
    response = views.search(request)
    assert b'Status : True' in response.content

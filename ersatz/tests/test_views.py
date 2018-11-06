import pytest

from django.test import Client
from django.contrib.auth.models import User
from ersatz.config import API, VIEWS_MSG_LOGIN, VIEWS_MSG_NO_FAV

################################################################################
#   ersatz.views.views.index()
################################################################################
def test_index():
    TEMPLATES = [
        'omega/home.html',
        'base.html',
        'omega/searchform.html',
        'omega/searchform.html',
    ]
    CLIENT = Client()
    response = CLIENT.get('/')

    assert TEMPLATES == [t.name for t in response.templates]
################################################################################


################################################################################
#   ersatz.views.views.search()
################################################################################
class TestSearch:
    """
    Non-regresion tests #27 : error if a search do not return products
    """
    CLIENT = Client()

    WITNESS = {
        'templates': [
            'ersatz/result.html',
            'base.html',
            'omega/searchform.html',
        ]
    }
    RESPONSE_EMPTY =  {'error': API['EMPTY'],'status': False}
    RESPONSE_NO_PROD =  {
        'error': API['NO_PROD'].format('foobar'),
        'status': False,
    }

    def fake_get_search_empty_context(self, request):
        """ ersatz.views.toolbox.get_search_context() fake function """
        return self.RESPONSE_EMPTY

    def fake_get_search_no_product_context(self, request):
        """ ersatz.views.toolbox.get_search_context() fake function """
        return self.RESPONSE_NO_PROD

    def test_empty_search(self, monkeypatch):
        self.WITNESS['response'] = self.RESPONSE_EMPTY

        monkeypatch.setattr('ersatz.views.toolbox.get_search_context', self.fake_get_search_empty_context)
        response = self.CLIENT.get('/ersatz/search/')

        assert response.status_code == 200
        assert self.WITNESS['templates'] == [t.name for t in response.templates]
        assert self.WITNESS['response']['error'] == response.context['error']

    def test_no_product_search(self, monkeypatch):
        self.WITNESS['response'] = self.RESPONSE_NO_PROD

        monkeypatch.setattr('ersatz.views.toolbox.get_search_context', self.fake_get_search_no_product_context)
        response = self.CLIENT.get('/ersatz/search/', {'s':'foobar'})

        assert response.status_code == 200
        assert self.WITNESS['templates'] == [t.name for t in response.templates]
        assert self.WITNESS['response']['error'] == response.context['error']

    def test_valid_search(self):
        """ Need to add a return in ersatz.views.toolbox.update_db for that """
        pass

################################################################################


################################################################################
#   ersatz.views.views.favorite_list()
################################################################################
class TestFavoriteList:
    CLIENT = Client()
    USER = {
        'username': 'jean',
        'password': 'jean',
        'email': 'jean@b.on',
    }
    TEMPLATES = [
        'ersatz/list.html',
        'base.html',
        'omega/searchform.html',
        'omega/searchform.html',
    ]

    def test_anonymous_user_favorite_list(self):
        response = self.CLIENT.get('/ersatz/list/')

        assert self.TEMPLATES == [t.name for t in response.templates]
        assert VIEWS_MSG_LOGIN in response.context['message']

    @pytest.mark.django_db
    def test_user_favorite_list_empty(self):
        self.CLIENT.force_login(
            User.objects.create(**self.USER)
        )
        response = self.CLIENT.get('/ersatz/list/')

        assert self.TEMPLATES == [t.name for t in response.templates]
        assert VIEWS_MSG_NO_FAV in response.context['message']
################################################################################

import pytest

from django.test import Client
from django.contrib.auth.models import User
from ersatz.config import VIEWS_MSG_LOGIN, VIEWS_MSG_NO_FAV

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

# Non-regresion test for issue #27 :
# - No DB storage if a search do not return products
# TODO : I'd like to test a HTTP response <200>, but `whitenoise` won't let me.
# TODO : see issue #28 for details.
# def fake_get_search_context(request):
    # """ ersatz.views.toolbox.get_search_context() fake function """
    # return {'status': False}

# def test_search_return_status_is_false(monkeypatch):
    # monkeypatch.setattr('ersatz.views.toolbox.get_search_context', fake_get_search_context)
    # response = views.search('This request will return `{status: False}`')
    # assert response.status_code == 200

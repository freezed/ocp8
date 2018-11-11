import json

import pytest

from django.core.exceptions import ObjectDoesNotExist
from django.test import Client
from django.contrib.auth.models import User
from ersatz.config import (API, VIEWS_ERR, VIEWS_MSG_CANDIDATE_NONE,
    VIEWS_MSG_LOGIN, VIEWS_MSG_NO_FAV)
from ersatz.models import Product, Favorite

################################################################################
#   ersatz.views.views.home()
################################################################################
def test_home():
    TEMPLATES = [
        'home.html',
        'base.html',
        'ersatz/searchform.html',
        'ersatz/searchform.html',
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
            'ersatz/no-result.html',
            'base.html',
            'ersatz/searchform.html',
            'ersatz/searchform.html',
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
        self.WITNESS.update({'response': self.RESPONSE_EMPTY})

        monkeypatch.setattr(
            'ersatz.views.toolbox.get_search_context',
            self.fake_get_search_empty_context
        )
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

    def fake_update_db(self, context):
        pass

    def fake_get_search_fromage_context(self, request):
        """ ersatz.views.toolbox.get_search_context() fake function """
        with open("ersatz/tests/samples/processed-fromage-page_1.json", "r") as json_file:
            context = json.load(json_file)

        return context

    @pytest.mark.django_db
    def test_valid_search(self, monkeypatch):
        TEMPLATES = [
            'ersatz/result.html',
            'base.html',
            'ersatz/searchform.html',
            'ersatz/pagination.html',
            'ersatz/pagination.html',
        ]
        BAD_FIELDS = [
            "<span class=\"nutri-badge\">False</span>",
            "src=\"False\"",
            "src=\"\"",
        ]
        monkeypatch.setattr(
            'ersatz.views.toolbox.get_search_context',
            self.fake_get_search_fromage_context
        )
        monkeypatch.setattr(
            'ersatz.views.toolbox.update_db',
            self.fake_update_db
        )

        response = self.CLIENT.get('/ersatz/search/', {'s':'fromage'})

        assert response.status_code == 200
        assert TEMPLATES == [t.name for t in response.templates]

        for bad_string in BAD_FIELDS:
            assert bad_string.encode() not in response.content
################################################################################


################################################################################
#   ersatz.views.views.candidates()
################################################################################
class FakeErsatzProduct:
    """  ersatz.views.toolbox.ErsatzProduct mock Class """
    def get_substitute_context():
        return {'status': False, 'message': VIEWS_MSG_CANDIDATE_NONE}

def mock_no_candidate_ersatz_product(code):
    """ ErsatzProduct mock function """
    return FakeErsatzProduct

def test_no_candidates(monkeypatch):
    monkeypatch.setattr(
        'ersatz.views.toolbox.ErsatzProduct',
        mock_no_candidate_ersatz_product
    )
    TEMPLATES = [
        'ersatz/no-candidates.html',
        'base.html',
        'ersatz/searchform.html',
        'ersatz/searchform.html',
    ]
    CLIENT = Client()
    response = CLIENT.get('/ersatz/candidates/1234567890')

    assert response.status_code == 200
    assert TEMPLATES == [t.name for t in response.templates]
    assert VIEWS_MSG_CANDIDATE_NONE == response.context['message']

def test_best_candidate():
    """ Need to populate DB to test this """
    pass

################################################################################


################################################################################
#   ersatz.views.views.favorite()
################################################################################
def test_no_favorite():
    TEMPLATES = [
        'ersatz/no-result.html',
        'base.html',
        'ersatz/searchform.html',
        'account/anonymous.html',
    ]
    CLIENT = Client()
    response = CLIENT.get('/ersatz/favorite/1234567890/9876543210/')

    assert response.status_code == 200
    assert TEMPLATES == [t.name for t in response.templates]
    assert VIEWS_MSG_LOGIN == response.context['error']

def test_saved_favorite():  # TODO
    """ DB populating is nedded to test this """
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

    @pytest.mark.django_db
    def test_anonymous_user_favorite_list(self):
        TEMPLATE_WITNESS = [
            'ersatz/list.html',
            'base.html',
            'ersatz/searchform.html',
            'ersatz/searchform.html',
        ]

        response = self.CLIENT.get('/ersatz/list/')

        assert TEMPLATE_WITNESS == [t.name for t in response.templates]
        assert VIEWS_MSG_LOGIN in response.context['message']

    @pytest.mark.django_db
    def test_user_favorite_list_empty(self):
        TEMPLATE_WITNESS = [
            'ersatz/list.html',
            'base.html',
            'ersatz/searchform.html',
            'ersatz/searchform.html',
        ]

        self.CLIENT.force_login(
            User.objects.create(**self.USER)
        )

        response = self.CLIENT.get('/ersatz/list/')

        assert TEMPLATE_WITNESS == [t.name for t in response.templates]
        assert VIEWS_MSG_NO_FAV in response.context['message']

    @pytest.mark.django_db
    def test_user_favorite_list_filled(self):
        TEMPLATE_WITNESS = [
            'ersatz/list.html',
            'base.html',
            'ersatz/searchform.html',
        ]

        with open("ersatz/tests/samples/processed-fromage-page_1.json", "r") as json_file:
            PRODUCTS = json.load(json_file)

        BAD_FIELDS = [
            "<span class=\"nutri-badge\">False</span>",
            "src=\"False\"",
            "src=\"\"",
        ]

        self.CLIENT.force_login(
            User.objects.create(**self.USER)
        )

        for product in PRODUCTS['products']:
            del(product['categories'])
            product['ingredients_text'] = product['ingredients_text'][:255]
            product['nutrition_grades'] = "z"

            if not product['image_front_thumb_url']:
                product['image_front_thumb_url'] = ''

            p = Product.objects.create(**product)

        FAVORITES = [
            {
                'products_id': Product.objects.get(code='3272770003148').id,
                'substitutes_id': Product.objects.get(code='3073786865191').id,
                'users_id': User.objects.get(username='jean').id,
            },
            {
                'products_id': Product.objects.get(code="3329770051133").id,
                'substitutes_id': Product.objects.get(code="4001724818908").id,
                'users_id': User.objects.get(username='jean').id,
            },
            {
                'products_id': Product.objects.get(code="3011250018308").id,
                'substitutes_id': Product.objects.get(code="7622300685782").id,
                'users_id': User.objects.get(username='jean').id,
            }
        ]

        for favorite in FAVORITES:
            Favorite.objects.create(**favorite)

        response = self.CLIENT.get('/ersatz/list/')

        assert TEMPLATE_WITNESS == [t.name for t in response.templates]

        for bad_string in BAD_FIELDS:
            assert bad_string.encode() not in response.content

################################################################################


################################################################################
#   ersatz.views.views.product()
################################################################################
class TestProduct:
    CLIENT = Client()
    base_tplt = [
        'base.html',
        'ersatz/searchform.html',
    ]
    PRODUCT = {
        'code': '1664',
        'image_front_thumb_url': 'https://via.placeholder.com/100x50?text=thumb_url',
        'image_front_url': 'https://via.placeholder.com/100x50?text=front_url',
        'image_nutrition_url': 'https://via.placeholder.com/100x50?text=nutrition_url',
        'ingredients_text': 'Wotch a kofee avec ton bibalaekaess et ta wurscht?',
        'name': 'Foo (Bar)',
        'nutrition_grades': 'c',
        'url': 'of url',
    }

    @pytest.mark.django_db
    def test_not_found_product(self):
        TEMPLATE_WITNESS = ['ersatz/no-result.html']
        TEMPLATE_WITNESS.extend(self.base_tplt)
        TEMPLATE_WITNESS.append('ersatz/searchform.html')

        response = self.CLIENT.get('/ersatz/product/1234567890')

        assert response.status_code == 200
        assert TEMPLATE_WITNESS == [t.name for t in response.templates]
        assert VIEWS_ERR.format(
            "Product matching query does not exist."
        ) in response.context['error']

    @pytest.mark.django_db
    def test_found_product(self):
        TEMPLATE_WITNESS = ['ersatz/product.html']
        TEMPLATE_WITNESS.extend(self.base_tplt)

        Product.objects.create(**self.PRODUCT)
        response = self.CLIENT.get('/ersatz/product/1664')

        assert response.status_code == 200
        assert TEMPLATE_WITNESS == [t.name for t in response.templates]

        for field, value in self.PRODUCT.items():
            assert value in  response.context['product'][field]
################################################################################

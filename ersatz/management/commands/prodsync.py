from django.core.management.base import BaseCommand

from ersatz.config import API, BASE_PRODUCT_FIELD
from ersatz.models import Product
from ersatz.views.toolbox import get_json


class Command(BaseCommand):
    help = 'Updates local products over OFF API'

    products = Product.objects.values().all()

    def changes(self, code):
        """ Check for a product update over OFF API """

        api_response = get_json(
            API['URL_PRODUCT'].format(code)
        )

        common_fields = {
            field: api_response['products'][field]
            # Only common fields between model & API
            # TODO : work on all models fields
            for field in BASE_PRODUCT_FIELD
            if field in api_response['products']
                # do not keep unchanged fields
                and api_response['products'][field] != list(self.products.values(field).filter(code=code))[0][field]
        }

        return common_fields

    def handle(self):
        pass

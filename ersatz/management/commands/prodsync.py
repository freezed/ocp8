import logging

from django.core.management.base import BaseCommand

from ersatz.config import API, BASE_PRODUCT_FIELD
from ersatz.models import Product
from ersatz.views.toolbox import get_json

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates local products over OFF API'

    products = Product.objects.values().all()

    def changes(self, code):
        """ Check for a product update over OFF API """

        api_response = get_json(
            API['URL_PRODUCT'].format(code)
        )

        # Only common fields between model & API. Do not keep unchanged fields
        # TODO : work on all models fields
        if 'product' in api_response:
            changes = {
                field: api_response['product'][field][:255]
                for field in BASE_PRODUCT_FIELD
                if field in api_response['product']
                    and api_response['product'][field][:255] != list(
                        self.products.values(field).filter(code=code)
                    )[0][field]
            }

            if len(changes) > 0:
                changes.update({'code': code})

        else:

            changes = {}

            logger.info('CRON Product not found', exc_info=True, extra={
                'EAN13': code,
            })
            print("KeyError: 'product' for code «{}»".format(code))

        return changes


    def dbupdate(self, changes):
        """ Updates DB products changes """
        Product.objects.filter(code=changes['code']).update(**changes)


    def handle(self, *args, **options):
        updated = []
        checked = []

        for prod in self.products:
            changed_prod = self.changes(prod['code'])

            if len(changed_prod) > 0:
                self.dbupdate(changed_prod)
                updated.append(prod)

                logger.info('CRON Product not found', exc_info=True, extra={
                    'EAN13': code,
                })

                print("updated : {}".format(changed_prod))

            else:
                checked.append(prod)

        logger.info('CRON finished', exc_info=True, extra={
            'prod_checked': len(checked),
            'prod_updated': len(updated),
            'prod_checked_list': checked,
            'prod_updated_list': updated,
        })
        print("CRON finished : checked {}, updated {}".format(
            len(checked), len(updated)
        ))

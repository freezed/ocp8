from django.core.management.base import BaseCommand

from ersatz.models import Product

class Command(BaseCommand):

    def dbproducts(self):
        products = Product.objects.values().all()

        return products


    def handle(self):
        pass

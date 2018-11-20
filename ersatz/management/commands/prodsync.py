from django.core.management.base import BaseCommand

from ersatz.models import Product

class Command(BaseCommand):

    products = Product.objects.values().all()


    def handle(self):
        pass

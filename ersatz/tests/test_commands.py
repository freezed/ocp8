import pytest
from ersatz.management.commands.prodsync import Command

def test_get_db_products():
    """ test a DB request to get products  """

    cmd_instance = Command()
    prods = cmd_instance.dbproducts()

    assert isinstance(prods, dict)
    assert prods[0]['code'] == '3073780258098'


""" for a product request api """


""" for an api response check if is differant than DB data """


""" update product in DB """


""" print updates summary """

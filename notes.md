# OCP8 - notes

## Console pastebin

    from django.contrib.auth.models import User;from ersatz.models import Favorite, Product, Category;uv = User.objects.values().get(id=1)

##  TODO

* in `` : `traceback['error'] = {'ConnectionError': pf(except_detail)}`

## Mess

```
# Static config
if os.environ.get('ENV') == 'PRODUCTION':

    # Static files settings
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

    # Extra places for collectstatic to find static files.
    STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, 'static'),
    )
```

---

    """
    >>> l = [
        {'products_id': 44, 'substitutes_id': 1924},
        {'products_id': 515, 'substitutes_id': 3126},
        {'products_id': 515, 'substitutes_id': 3127},
        {'products_id': 575, 'substitutes_id': 544},
        {'products_id': 575, 'substitutes_id': 546},
        {'products_id': 575, 'substitutes_id': 548},
    ]
    {44: [1924], 515: [3126, 3127], 575: [544, 546, 548]}
    """

    favorite_list = Favorite.objects.values(
        'products_id', 'substitutes_id'
    ).filter(users=1).order_by('products_id')

    favorite_dict = {}

    for idx, favorite in enumerate(favorite_list):
        if idx != 0
            and fav['products_id'] == favorite_list[idx-1]['products_id']:
            favorite_dict[fav['products_id']].append(fav['substitutes_id'])
        else:
            favorite_dict[fav['products_id']] = [fav['substitutes_id']]

---

```
class UserSession(User):
    """ Class doc """

    def __init__(self, request_user_id):
        """ Class initialiser """
        self.uid = request_user_id
```

---

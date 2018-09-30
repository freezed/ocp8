Documentation
=============

**Note** : _Check latest version of this doc on [github](https://github.com/freezed/ocp8/blob/master/doc/documentation.md)._

---

## Dependencies

- `django 2.1.1`
- `requests 2.19.1`
- `gunicorn 19.9.0` (only for running on [Heroku][heroku])
- `python 3.6.6`

## Development tools used

- `coverage 4.5.1`
- `pytest 3.8.1`
- `pytest-cov 2.6.0`
- `pytest-django 3.4.3`

## Runs

- on [Heroku][heroku]
    - `heroku CLI v7.16.0 linux-x64 node-v10.10.0`
    - with `gunicorn 19.9.0`

## Installation

1. get the code : `git clone git@github.com:freezed/ocp8.git`
2. create a dedicated virtualenv : `python3 -m venv .venv`
3. starts virtualenv  : `source .venv/bin/activate`
4. adds dependencies : `cd ocp8; pip install -r requirements.txt`
5. [config DB - TODO #5][05]
6. Breathe…
7. run tests : `pytest`
8. run test coverage : `pytest --cov-config .coveragerc --cov=omega --cov=account --cov=ersatz test_*.py;`
9. run developement server : `.manage.py runserver`

## File organisation

**Django project name :**
- omega

**Djano apps :**

- account
- ersatz

### Tree

    ├── account
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── templates
    │   │   └── account
    │   │       └── home.html
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── ersatz
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── api.py
    │   ├── apps.py
    │   ├── config.py
    │   ├── migrations
    │   ├── models.py
    │   ├── templates
    │   │   └── ersatz
    │   │       ├── home.html
    │   │       └── result.html
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── issues
    ├── LICENSE
    ├── manage.py
    ├── omega
    │   ├── __init__.py
    │   ├── forms.py
    │   ├── settings.py
    │   ├── templates
    │   │   ├── base.html
    │   │   ├── omega
    │   │   │   └── home.html
    │   │   └── registration
    │   │       ├── logged_out.html
    │   │       ├── login.html
    │   │       ├── password_change_form.html
    │   │       ├── password_reset_form.html
    │   │       └── signin.html
    │   ├── test.py
    │   ├── urls.py
    │   ├── views.py
    │   └── wsgi.py
    ├── Procfile
    ├── pytest.ini
    ├── README.md
    └── requirements.txt



[heroku]: https://heroku.com
[05]: https://github.com/freezed/ocp8/issues/5

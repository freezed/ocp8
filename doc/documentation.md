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
    - `heroku/7.16.6 linux-x64 node-v10.11.0`
    - with `gunicorn 19.9.0`

## Installation

1. get the code : `git clone git@github.com:freezed/ocp8.git`
2. create a dedicated virtualenv : `python3 -m venv .venv`
3. starts virtualenv  : `source .venv/bin/activate`
4. adds dependencies : `cd ocp8; pip install -r requirements.txt`
5. creates a `postgresql` DB
6. Edit [`omega/settings.py`][settings]
7. run tests : `pytest`
8. run test coverage : `pytest --cov=omega --cov=ersatz`
9. run developement server : `./manage.py runserver`

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

## Physical data model

Table `auth_user` is from built-in django authentification model

![PMD image](https://raw.githubusercontent.com/freezed/ocp8/master/doc/pdm.png)

[PUML sources](https://github.com/freezed/ocp8/blob/master/doc/pdm.puml)


[heroku]: https://heroku.com
[settings]: https://github.com/freezed/ocp8/blob/3a1bc304537fa1b51b1d98fd9ad95e140efb02e5/omega/settings.py#L84

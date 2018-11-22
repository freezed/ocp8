Documentation
=============

**Note** : _Check latest version of this doc on [github][doc]._

---

## Dependencies

- `django 2.1.1`
- `dj-database-url 0.5.0`
- `gunicorn 19.9.0` (only for running on [Heroku][heroku])
- `psycopg2-binary 2.7.5`
- `python 3.6.6`
- `requests 2.20.0`
- `whitenoise 4.1`

## Development tools used

- `coverage 4.5.1`
- `pytest 3.8.1`
- `pytest-cov 2.6.0`
- `pytest-django 3.4.3`

## Runs

- on [Heroku][heroku]
    - `heroku/7.18.5 linux-x64 node-v11.0.0`
    - with `gunicorn 19.9.0`

## Installation

1. get the code : `git clone git@github.com:freezed/ocp8.git`
2. create a dedicated virtualenv : `python3 -m venv .venv`
3. starts virtualenv  : `source .venv/bin/activate`
4. adds dependencies : `cd ocp8; pip install -r requirements.txt`
5. creates a `postgresql` DB
6. Edit [`omega/settings.py`][settings]
7. set DB : `./manage.py migrate`
8. run tests : `pytest --cov=omega --cov=ersatz`
9. run developement server : `./manage.py runserver`

## File organisation

**Django project name :**

- omega

**Django apps :**

- account (user account, login, signup, etc.)
- ersatz (all about products, substitutes, favorites, etc.)

### Tree

    ├── account
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── templates
    │   │   ├── about.html
    │   │   ├── account
    │   │   │   ├── account.html
    │   │   │   └── anonymous.html
    │   │   ├── home.html
    │   │   └── registration
    │   │       ├── logged_out.html
    │   │       ├── login.html
    │   │       ├── password_change_form.html
    │   │       ├── password_reset_form.html
    │   │       └── signin.html
    │   ├── tests.py
    │   └── views.py
    ├── doc
    │   ├── approach.md
    │   ├── documentation.md
    │   ├── pdm.png
    │   ├── pdm.puml
    │   ├── PITCHME.md
    │   └── template-grid.jpg
    ├── ersatz
    │   ├── admin.py
    │   ├── apps.py
    │   ├── config.py
    │   ├── migrations
    │   │   └── …
    │   ├── models.py
    │   ├── templates
    │   │   └── ersatz
    │   │       ├── candidates.html
    │   │       ├── favorite.html
    │   │       ├── list.html
    │   │       ├── no-candidates.html
    │   │       ├── no-result.html
    │   │       ├── pagination.html
    │   │       ├── product.html
    │   │       ├── result.html
    │   │       └── searchform.html
    │   ├── tests
    │   │   ├── samples
    │   │   │   ├── api-fromage-page_1.json
    │   │   │   └── processed-fromage-page_1.json
    │   │   ├── test_toolbox.py
    │   │   └── test_views.py
    │   ├── urls.py
    │   └── views
    │       ├── toolbox.py
    │       └── views.py
    ├── omega
    │   ├── settings.py
    │   ├── static
    │   │   ├── favicon.ico
    │   │   ├── img
    │   │   │   └── …
    │   │   ├── sbtstrp-creative-css
    │   │   │   └── …
    │   │   ├── sbtstrp-creative-js
    │   │   │   └── …
    │   │   ├── sbtstrp-creative-scss
    │   │   │   └── …
    │   │   └── sbtstrp-creative-vendor
    │   │       └── …
    │   ├── templates
    │   │   ├── 404.html
    │   │   ├── 500.html
    │   │   └── base.html
    │   ├── urls.py
    │   └── wsgi.py
    ├── staticfiles
    │   ├── admin
    │   │   └── …
    │   ├── favicon.ico
    │   ├── img
    │   │   └── …
    │   ├── sbtstrp-creative-css
    │   │   └── …
    │   ├── sbtstrp-creative-js
    │   │   └── …
    │   ├── sbtstrp-creative-scss
    │   │   └── …
    │   ├── sbtstrp-creative-vendor
    │   │   └── …
    │   └── staticfiles.json
    ├── LICENSE
    ├── manage.py
    ├── Procfile
    ├── pytest.ini
    ├── README.md
    └── requirements.txt

## Physical data model

Table `auth_user` is from built-in django authentification model

![PMD image](https://raw.githubusercontent.com/freezed/ocp8/v0.3/doc/pdm.png)

[PUML sources](https://github.com/freezed/ocp8/blob/v0.3/doc/pdm.puml)


[doc]: https://github.com/freezed/ocp8/blob/master/doc/documentation.md
[heroku]: https://heroku.com
[settings]: https://github.com/freezed/ocp8/blob/v0.3/omega/settings.py#L84

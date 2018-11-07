# [PyDev] Project 11

---

# Introduction

+++

###### Improve one of the projects already completed

@ul

- use tests (unit & functional)
- use github
- fake conversation with client

@ulend

---

# Workflow

@ul

 - **think**, **sketch** & **draft** (features, functions, needed tools)
 - **gather** things in autonomous packages
 - **organize** the work (with a _kanban type_ table)
 - write **tests**
 - write **code**

@ulend

---

# Overview

+++

I known the code well : I work on it for a month, but as I am learning _Django_ on the way, I had to deal with odd choices & stranges implementations when I meet old code…

+++

#### the _Django_ tree

At start it took some time to understand the logic of the bricks position/role, and now I have a more accurate view on what must be where. Then the first improvement was to reorganize the file tree, here is the job :

+++

`omega` :

@ul

* keep errors & base templates, move all others
* keep all statics
* exports all tests & views
* disabling admin interface
* harmonize `auth` routes names

@ulend

+++

`account` :

@ul

* harmonize routes names
* host most of ex-`omega` templates
* no `urls.py` : no need to prefix URL with `account`

@ulend

+++

`ersatz` :

@ul

* host `searchform.html`
* remove unused `home.html`

@ulend

---

```
├── omega
│   ├── settings.py
│   ├── static
│   │   └── …
│   ├── templates
│   │   ├── 404.html
│   │   ├── 500.html
│   │   └── base.html
│   ├── urls.py
│   └── wsgi.py
├── account
│   ├── apps.py
│   ├── forms.py
│   ├── templates
│   │   ├── about.html
│   │   ├── account
│   │   │   ├── account.html
│   │   │   └── anonymous.html
│   │   ├── home.html
│   │   └── registration
│   │       ├── login.html
│   │       ├── …
│   │       └── signin.html
│   ├── tests.py
│   └── views.py
├── doc
│   └── …
├── ersatz
│   ├── admin.py
│   ├── apps.py
│   ├── config.py
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
└── manage.py
```

+++

#### Testing in _Django_ context

I decided to use `django-pytest`, in a minimal way. Here it is to use some database features with tests.

+++?code=ersatz/tests/samples/processed-fromage-page_1.json&title=Fake data

@[49](Missing URL)
@[170](Missing nutriscore)
@[181](Empty URL)
@[242](Empty URL)

+++?code=ersatz/tests/test_views.py&title=View rendering tests

@[90-100](Setting expected values)
@[101-107](Mocking data)
@[80-88](Data from JSON sample)
@[110-116](Testing)

+++

#### Stay in the scope

As always working on light specifications is delicate. Do the job asked for, add requested feature even if they are sometime implicit. Do not over estimate the client needs.

---

# Future…

* Failover to `API` if no found in DB
* Full tests implementation (DB & Selelnium)
* Local & distant DB conflict (stay up to date w/ cron)
* Improve substitution match
* … and more : have a look to [issues](https://github.com/freezed/ocp8/issues/)

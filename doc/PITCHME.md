# Approach pitch

###### [PyDev] Project 8

---

# Introduction

+++

###### Propose a service using **OpenFoodFacts** data to find a products and it's better substitutes with these characteristics :

@ul

- use _Django_
- use _PostgreSQL_
- deploy on an _Heroku_ instance **connected** to _GitHub_

@ulend

+++

##### Personal background

+++

#### 1st experiences

@ul

- build a _Django_ project (!)
- using an _ORM_
- talking with _PostgreSQL_
- wearing _Bootstrap_

@ulend

+++

#### Known things

@ul

- testing basics
- **OpenFoodFacts** API response
- basic _Heroku_ usage
- comprehension list, dict, foo, … <3

@ulend

---

# Workflow

@ul

 - **think**, **sketch** & **draft** (features, functions, needed tools)
 - **gather** things in autonomous packages
 - **organize** the work (with a _kanban type_ table)
 - write **tests**
 - write **code**
 - **…repeat**
 - **wrap** with _Bootstrap_

@ulend

---

# Overview

+++

###### Take in hand the tools & play with it

* **OpenFoodFacts** `API` : Choosing useful fields
* _pytest_ : django integration with coverage
* _Heroku_ : DB & statics features

+++

###### Build a minimalist _Django_ app

@ul

* 1st : the most minimal **Hello world** possible
* then push **atomic commits** one by one

@ulend

+++?code=omega/forms.py&title=Model User [`omega/forms.py`]

@[1-3](Use built-in auth & user model)
@[6-10](Pick only desired fields)

+++?code=ersatz/tests/tests.py&title=Testing [`ersatz/tests/tests.py`]

@[12-18](Testing user request : fake django response)
@[20-26](Invalid user request : testing)
@[29-36](Valid user request : fake API response)
@[38-43](Valid user request : testing)
@[128-140](Processing products : mocking API data with JSON files)
@[142-148](Processing products : testing)
@[166-179](Non-regression tests)

+++

![PDM image](doc/pdm.png)

+++

###### Define models

+++?code=ersatz/models.py&title=Product [`ersatz/models.py`]

@[12-17](A piece of doc)
@[18-28](Original fields)
@[28-35](Special fields)

+++?code=ersatz/config.py&title=Product [`ersatz/config.py`]

@[4](Import Product)
@[17-24](Harvest models)
@[26-31](Adding specials)

+++?code=ersatz/views/toolbox.py&title=SearchProduct [`ersatz/views/toolbox.py`]

@[222-223](API response processing)
@[229-235](Is API response looking usefull?)
@[243-249](Get wanted fields)
@[250-253](Set missing fields to False)
@[255-256](Call methods for special fields)
@[332-351](Generating product name)
@[258-265](Return API response processed)

+++

###### Template nesting

![template grid image](doc/template-grid.jpg)

---

# Difficulties encountered

+++

#### 1. Testing in _Django_ context

_Django_ organization is a bit more complex than flask (!), it provides dedicated tools and some specific packages are avaiable. I decided to use `django-pytest`, in a minimal way (only units tests). Next step is going further to complete testing tools for _Django_.

+++

#### 2. Discovering _Bootstrap_

I never used it before, so it took me a few days to get an overview of the possibilities offered by this tool (grid, fontawesome, etc.). Finally it was not so hard after a few days, but the template usage simplifies the discovering.

+++

#### 3. Organizing _Django_ tree

App, project, views, template, built-ins, etc. It took some time to understand the logic of the bricks position/role. Next step is to migrates code from `account` to `ersatz` app, at start I though that a separation was a good idea, actually it is not the case.

+++

```
├── omega
│   ├── forms.py
│   ├── settings.py
│   ├── static
│   │   ├── favicon.ico
│   │   ├── img
│   │   ├── sbtstrp-creative-css
│   │   │   └── …
│   │   ├── sbtstrp-creative-js
│   │   │   └── …
│   │   ├── sbtstrp-creative-scss
│   │   │   └── …
│   │   └── sbtstrp-creative-vendor
│   │       └── …
│   ├── templates
│   │   ├── base.html
│   │   ├── omega
│   │   └── registration
│   ├── test.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── account
│   ├── templates
│   │   └── account
│   │       ├── anonymous.html
│   │       └── home.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── ersatz
│   ├── config.py
│   ├── migrations
│   │   └── …
│   ├── models.py
│   ├── templates
│   │   └── ersatz
│   │       ├── candidates.html
│   │       ├── favorite.html
│   │       ├── home.html
│   │       ├── list.html
│   │       ├── no-candidates.html
│   │       ├── no-favorite.html
│   │       ├── pagination.html
│   │       ├── product.html
│   │       └── result.html
│   ├── tests
│   │   ├── samples
│   │   │   ├── api-fromage-page_1.json
│   │   │   └── processed-fromage-page_1.json
│   │   └── tests.py
│   │
│   ├── urls.py
│   └── views.py
│        ├── toolbox.py
│        └── views.py
├── LICENSE
├── manage.py
├── Procfile
├── pytest.ini
├── README.md
└── requirements.txt
```

+++

#### 4. Stay in the scope

As always working on light specifications is delicate. Do the job asked for, add requested feature even if they are sometime implicit. Do not over estimate the client needs.

---

# Future…

* Failover to `API` if no found in DB
* Full tests implementation (DB & Selelnium)
* Local & distant DB conflict (stay up to date w/ cron)
* Improve substitution match
* … and more : have a look to [issues](https://github.com/freezed/ocp8/issues/)

-[_Courses Open Classrooms_][oc]-

# [PyDev] Project 8

_Last version of this document is available on [Github][approach]._
_kanban table project is avaiable [on GitHub][kanban] _

## Approach

### Introduction

Propose a service using [OpenFoodFacts][OFF] data to find a products and it's better substitutes with these characteristics :

- use [Django][django]
- use [PostgreSQL][postgres]
- deploy on a [Heroku][heroku] account connected to [Github][gither]

The whole exercise description is available on [OpenClassrooms site][oc], the project is hosted on [Github][kanban] and it is deployed [here][herokuapp].


### Workflow

 - plan : features, scripts, files, functions, tools needed
 - create [features][features], grouped in autonomous packages
 - organize with a [_kanban type_ table][kanban]
 - write tests with [`pytest`][pytest]
 - write code
 - integrate a [Bootstrap][bootstrap]


### Code construction

To build the script, I followed this approach :

1. take in hand the tools & play with it : [OpenFoodFacts][OFF] `API`, [Django][django], [`pytest`][pytest] & [Heroku][heroku]
2. build a minimalist [Django][django] app, and add feature only step by step
3. use built-in authentication & user model
4. build 1st tests on API response & data processing
5. set minimalist templating
6. add DB storage
7. connecting models auth_user/ersatz
8. learn [Bootstrap][bootstrap] to integrate template


### Code organization

**_Django_ project name :**
- omega

**_Django_ apps :**
- account
- ersatz

### Difficulties encountered

#### 1. Testing in _Django_ context

_Django_ organization is a bit more complex than flask (!), it provides dedicated tools and some specific packages are avaiable. I decided to use `django-pytest`, in a minimal way (only units tests). Next step is going further to complete testing tools for _Django_.

#### 2. Discovering [Bootstrap][bootstrap]

I never used it before, so it took me a few days to get an overview of the possibilities offered by this tool (grid, fontawesome, etc.). Finally it was not so hard after a few days, but the template usage simplifies the discovering.

#### 3. Organizing _Django_ tree

App, project, views, template, built-ins, etc. It took some time to understand the logic of the bricks position/role. Next step is to migrates code from `account` to `ersatz` app, at start I though that a separation was a good idea, actually it is not the case.

#### 4. Stay in the scope

As always working on light specifications is delicate. Do the job asked for, add requested feature even if they are sometime implicit. Do not over estimate the client needs.


### Possible [developments][issues]

* [Export code from `account` to `ersatz` app][39]
* [Full tests implementation][40]
* [Local & distant DB conflict][36]
* [Product matching query does not exist][33]
* [ConnectionError exception is not properly catched][32]
* [Catch DB error if migration is not done][30]
* [Failover to API if no ersatz found in DB][29]
* [Add `fake_get_json_count_zero()`][24]

[24]: https://github.com/freezed/ocp8/issues/24
[29]: https://github.com/freezed/ocp8/issues/29
[30]: https://github.com/freezed/ocp8/issues/30
[32]: https://github.com/freezed/ocp8/issues/32
[33]: https://github.com/freezed/ocp8/issues/33
[36]: https://github.com/freezed/ocp8/issues/36
[39]: https://github.com/freezed/ocp8/issues/39
[40]: https://github.com/freezed/ocp8/issues/40
[approach]: https://github.com/freezed/ocp8/blob/master/doc/approach.md
[bootstrap]: https://github.com/twbs/bootstrap
[django]: https://www.djangoproject.com/
[features]: https://github.com/freezed/ocp8/issues?utf8=%E2%9C%93&q=is%3Aissue+label%3Afeature+is%3Aclosed+
[gither]: https://devcenter.heroku.com/articles/github-integration
[herokuapp]: https://ocp8-1664.herokuapp.com/
[heroku]: https://devcenter.heroku.com/articles/getting-started-with-python
[issues]: https://github.com/freezed/ocp8/issues
[kanban]: https://github.com/freezed/ocp8/projects/1
[log]: http://flask.pocoo.org/docs/1.0/logging/#logging
[oc]: https://openclassrooms.com/fr/projects/creez-grandpy-bot-le-papy-robot "Créez une plateforme pour amateur de pâte à tartiner"
[OFF]: http://fr.openfoodfacts.org/
[postgres]: https://www.postgresql.org/
[pytest]: https://pytest.org "Helps you write better programs"
[ottg]: https://www.obeythetestinggoat.com
[selenium]: http://www.seleniumhq.org/

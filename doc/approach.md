-[_Courses Open Classrooms_][oc]-

# [PyDev] Project 11

_Last version of this document is available on [Github][approach]._

_Kanban table project is available [on GitHub][kanban]_

---

## Approach

### Introduction

Improve an old project you have made using tests (unit & functional)

- use [github][kanban]
- fake [conversation with client][mail]

The whole exercise description is available on [OpenClassrooms site][oc], the project is hosted on [Github][kanban] and it is deployed [here][herokuapp].


### Workflow

 - plan : features, scripts, files, functions, tools needed
 - create [features][features], grouped in autonomous packages
 - organize with a [_kanban type_ table][kanban]
 - write tests with [`pytest`][pytest]
 - write code


### Code organization

**_Django_ project name :**
- omega

**_Django_ apps :**
- account (user account, login, sign-up, etc.)
- ersatz (all about products, substitutes, favorites, etc.)


### Overview

I known the code well, I work on it for a month, but as I am learning _Django_ on the way, I had to deal with odd choices & stranges implementations when I meet old code…

#### the _Django_ tree

At start it took some time to understand the logic of the bricks position/role, and now I have a more accurate view on what must be where. Then the first improvement was to reorganize the file tree, here is the job :

Project `omega` :

* keep errors & base templates, move all others
* keep all statics
* exports all tests & views
* disabling admin interface
* rename `/my/*` routes

App `account` :

* rename some routes
* host most of ex-`omegega` templates
* no `urls.py` : no need to prefix URL with `account`

App `ersatz` :

* host `searchform.html`
* remove unused `home.html`


#### Testing in _Django_ context

_Django_ provides dedicated tools and some specific packages are available. I decided to use `django-pytest`, in a minimal way. Here it is to use some database features with tests. The subject is wide, even if there are still some to discover, I have learned a lot.


#### Stay in the scope

As always working on light specifications is delicate. Do the job asked for, add requested feature even if they are sometime implicit. Do not over estimate the client needs.


### Possible [developments][issues]

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
[40]: https://github.com/freezed/ocp8/issues/40
[approach]: https://github.com/freezed/ocp8/blob/master/doc/approach.md
[bootstrap]: https://github.com/twbs/bootstrap
[django]: https://www.djangoproject.com/
[features]: https://github.com/freezed/ocp8/issues?utf8=%E2%9C%93&q=is%3Aissue+label%3Afeature+is%3Aclosed+
[gither]: https://devcenter.heroku.com/articles/github-integration
[herokuapp]: https://ocp8-1664.herokuapp.com/
[heroku]: https://devcenter.heroku.com/articles/getting-started-with-python
[issues]: https://github.com/freezed/ocp8/issues
[kanban]: https://github.com/freezed/ocp8/projects/2
[log]: http://flask.pocoo.org/docs/1.0/logging/#logging
[mail]: https://github.com/freezed/ocp8/blob/v0.3/doc/chat-history.md
[oc]: https://openclassrooms.com/fr/projects/ameliorez-un-projet-existant-en-python "Créez une plateforme pour amateur de pâte à tartiner"
[OFF]: http://fr.openfoodfacts.org/
[postgres]: https://www.postgresql.org/
[pytest]: https://pytest.org "Helps you write better programs"
[ottg]: https://www.obeythetestinggoat.com
[selenium]: http://www.seleniumhq.org/

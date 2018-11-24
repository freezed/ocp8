-[_Courses Open Classrooms_][oc]-

# [PyDev] Project 10

_Last version of this document is available on [Github][approach]._

_Kanban table project is available [here][kanban]._

---

## Approach

### Introduction

This is a web application proposing to find a healthy substitute for a chosen food. So far, I deployed the application using a _PaaS solution_, now I must :

1. host it on a _VPS_
1. implement _CI_
1. monitor the server
1. log application activity
1. use `cron` to plan a maintenance task

_Personal bonus_:

* Automated deployment in a staging environment via _Heroku_ after successful testing

### 1. Hosting

Using a [Digital Ocean][do] _VPS_ running a [Debian/Stretch][debian] (stable). Django config is made with environment variables :

`omega.settings` :

    ├── __init__.py
    ├── production.py
    ├── stage.py
    └── travis.py

Developpement settings are sets  in `__init__.py` other files are activated via the `DJANGO_SETTINGS_MODULE` _env var_.

Application is served through this software chain :

* `supervisor` runs the `django wsgi application` on a supervised process (with corresponding configuration)

```shell
user@ocp10:~$ cat /etc/supervisor/conf.d/ocp10-gunicorn.conf
[program:ocp10-gunicorn]
command = /home/user/ocp8/.venv/bin/gunicorn omega.wsgi:application
user = user
directory = /home/user/ocp8
autostart = true
autorestart = true
environment = DJANGO_SETTINGS_MODULE='omega.settings.production'
```

[ [see `supervisor` config][imgsupervisor] ]

* `gunicorn` connects the `django app` to `nginx` HTTP server
* `nginx` serves client requests over network (Internet) & static files :

```shell
user@ocp10:~$ cat /etc/nginx/sites-available/ocp10
(…)
location /static {
    alias /home/user/ocp8/staticfiles/;
}
(…)
```

[ [see `nginx` config][imgnginx] ]

### 2. Continuous Integration

_Travis CI_ manage the integration & optional delivery

##### Build staging flow (bonus)

![Staging CI/CD flow - image][imgstaging]

##### Build production flow

![Production integration - image][imgproduction]

##### Screenshots

[ [see `travis CI` build][imgtravis1] ]

[ [see `travis CI` detail][imgtravis2] ]

### 3. Monitoring

_Digital Ocean_ provides built in server monitoring on :

* CPU charge
* Memory alocation
* Disk access/usage
* Used bandwith
* … and process hierarchy

[ [see server monitoring - dashboard][imgmonit1] ]

[ [see server monitoring - mail alert][imgmonit2] ]

### 4. Logging

_Sentry_ let you put snippets in your code acting like sensors, then you can log anything you want : a new search, unknown product, etc.

You can creates projects, connect a `git` repo to connect errors & code version (commits). A mail alert is also avaiable.

![Server logging - image][imglogging2] ]

[ [see `sentry.io` projects][imglogging1] ]

[ [see `sentry.io` versions][imglogging3] ]

[ [see `sentry.io` mail alert][imglogging4] ]

### 5. cronjob

Each days @ 0305, `cron` runs the DB syncronisation :

```shell
user@ocp10:~$ crontab -l
5  3  *  *  * user /home/user/ocp10-django-dbsync.sh

user@ocp10:~$ cat ocp10-django-dbsync.sh
#!/bin/bash
# cp10-django-dbsync.sh :
# Runs a Django DB synchronization

export DJANGO_SETTINGS_MODULE='omega.settings.production'
source /home/user/ocp8/.venv/bin/activate
python3 /home/user/ocp8/manage.py prod
```

##### Screenshots

[ [see `cronjob` config][imgcronjob1] ]

[ [see `cronjob` update log][imgcronjob2] ]

## [Future][issues]…

* setting [automated deployment][68] for production
* improving [cronjob tests][65]
* improving [cronjob][44]


[44]: https://github.com/freezed/ocp8/issues/44
[65]: https://github.com/freezed/ocp8/issues/65
[68]: https://github.com/freezed/ocp8/issues/68
[approach]: https://github.com/freezed/ocp8/blob/v0.4/doc/approach.md
[debian]: https://debian.org
[do]: https://www.digitalocean.com
[imgcronjob1]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/51-cronjob.jpg "Click to see screenshot"
[imgcronjob2]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/52-cronjob.jpg "Click to see screenshot"
[imglogging1]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/41-sentry-projects.png "Click to see screenshot"
[imglogging2]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/42-sentry-issues.png "Click to see screenshot"
[imglogging3]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/43-sentry-version.png "Click to see screenshot"
[imglogging4]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/44-sentry-mail.jpg "Click to see screenshot"
[imgmonit1]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/31-do-monit.jpg "Click to see screenshot"
[imgmonit2]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/32-do-monit.jpg "Click to see screenshot"
[imgnginx]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/12-nginx.jpg "Click to see screenshot"
[imgproduction]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/21-build-flow-production.jpg
[imgstaging]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/22-build-flow-staging.jpg
[imgsupervisor]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/11-supervisor.jpg "Click to see screenshot"
[imgtravis1]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/23-travis-builds.jpg "Click to see screenshot"
[imgtravis2]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/24-travis-details.jpg "Click to see screenshot"
[issues]: https://github.com/freezed/ocp8/issues
[kanban]: https://github.com/freezed/ocp8/projects/3
[oc]: https://openclassrooms.com/fr/projects/ameliorez-un-projet-existant-en-python "Créez une plateforme pour amateur de pâte à tartiner"

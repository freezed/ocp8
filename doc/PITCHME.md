-_Courses Open Classrooms_-

# [PyDev] Project 10

---

-_Introduction_-

This is a web application proposing to find a healthy substitute for a chosen food. So far, I deployed the application using a _PaaS solution_, now I must :

@ol

1. host it on a _VPS_
1. implement _CI_
1. monitor the server
1. log application activity
1. use `cron` to plan a maintenance task
1. [_Personal bonus_] auto-deploy staging  on _Heroku_ after

@olend

---

## 1. Hosting

A _Digital Ocean_ VPS running a _Debian/Stretch_.

![Droplet Digital Ocean screenshoot](doc/img/30-do-dropplet.png)

+++

Configuration is made with environment variables :

`omega.settings` :

    ├── __init__.py
    ├── production.py
    ├── stage.py
    └── travis.py

+++

Developpement settings are sets  in `__init__.py` other files are activated via the `DJANGO_SETTINGS_MODULE` _env var_.

+++

Application is served through this software chain :

* `supervisor` runs the `django wsgi application` on a supervised process (with corresponding configuration)

+++

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
+++

@ul

1. `gunicorn` connects the `django app` to `nginx` HTTP server
2. `nginx` serves client requests over network (Internet) & static files :

@ulend

```shell
user@ocp10:~$ cat /etc/nginx/sites-available/ocp10
(…)
location /static {
    alias /home/user/ocp8/staticfiles/;
}
(…)
```
---

## 2. Continuous Integration

_Travis CI_ manage the integration & optional delivery

+++

### Build staging flow (bonus)

![Staging CI/CD flow - image][imgstaging]

+++

### Build production flow

![Production integration - image][imgproduction]

+++

![see `travis CI` build][imgtravis1]

![see `travis CI` detail][imgtravis2]

+++

## 3. Monitoring

_Digital Ocean_ provides built in server monitoring on :

@ul

* CPU charge
* Memory alocation
* Disk access/usage
* Used bandwith
* … and process hierarchy

@ulend

+++

![see server monitoring - dashboard][imgmonit1]

+++

![see server monitoring - mail alert][imgmonit2]

---

## 4. Logging

![Server logging - image][imglogging2]

+++

![`sentry.io` projects][imglogging1]

+++

![`sentry.io` versions][imglogging3]

+++

![`sentry.io` mail alert][imglogging4]

---

## 5. cronjob

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
+++

![`cronjob` update log][imgcronjob2]

---

## Future…

* setting [automated deployment][68] for production
* improving [cronjob tests][65]
* improving [cronjob][44]

[44]: https://github.com/freezed/ocp8/issues/44
[65]: https://github.com/freezed/ocp8/issues/65
[68]: https://github.com/freezed/ocp8/issues/68

[imgcronjob1]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/51-cronjob.jpg "Click to see screenshot"
[imgcronjob2]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/52-cronjob.jpg "Click to see screenshot"
[imglogging1]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/41-sentry-projects.png "Click to see screenshot"
[imglogging2]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/42-sentry-issues.png "Click to see screenshot"
[imglogging3]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/43-sentry-version.png "Click to see screenshot"
[imglogging4]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/44-sentry-mail.jpg "Click to see screenshot"
[imgmonit1]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/31-do-monit.jpg "Click to see screenshot"
[imgmonit2]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/32-do-monit.jpg "Click to see screenshot"
[imgnginx]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/12-nginx.jpg "Click to see screenshot"
[imgproduction]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/21-build-flow-production.jpg
[imgstaging]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/22-build-flow-staging.jpg
[imgsupervisor]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/11-supervisor.jpg "Click to see screenshot"
[imgtravis1]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/23-travis-builds.jpg "Click to see screenshot"
[imgtravis2]: https://raw.githubusercontent.com/freezed/ocp8/wip-doc/doc/img/24-travis-details.jpg "Click to see screenshot"

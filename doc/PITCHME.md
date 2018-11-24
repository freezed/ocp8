-_Courses Open Classrooms_-

# [PyDev] Project 10

+++

### So far, this application is using a _PaaS tool_, it's time to…

@ul

* host it on a _VPS_
* implement _CI_
* monitor the server
* log application activity
* use `cron` to plan a maintenance task
* [_Personal bonus_] auto-deploy staging  on _Heroku_ after

@ulend

---

## 1. Hosting

A _Digital Ocean_ VPS running a _Debian/Stretch_.

![Droplet Digital Ocean screenshoot](doc/img/30-do-dropplet.png)

+++

@ul

* Developpement settings are sets  in `__init__.py`
* … overridden via _env var_ «`DJANGO_SETTINGS_MODULE`»

@ulend

`omega.settings` :

    ├── __init__.py
    ├── production.py
    ├── stage.py
    └── travis.py
+++

`supervisor` runs the `django wsgi application`

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

`user@ocp10:~$ cat /etc/nginx/sites-available/ocp10`

```shell
(…)
location /static {
    alias /home/user/ocp8/staticfiles/;
}
(…)
```

@ul

* `gunicorn` connects the `django app` to `nginx` HTTP server
* `nginx` serves client requests over network (Internet) & static files :

@ulend

---

## 2. Continuous Integration

_Travis CI_ manage the integration & optional delivery

![Staging CI/CD flow - image](doc/img/20-travis.png)

+++

### Build staging flow (bonus)

![Production integration - image](doc/img/22-build-flow-staging.jpg)

### Build production flow

![Staging CI/CD flow - image](doc/img/21-build-flow-production.jpg)

+++

![see `travis CI` build](doc/img/23-travis-builds.jpg)


---

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

![31-do-monit.jpg](doc/img/31-do-monit.jpg)

+++

##### Mail alerts

![32-do-monit.jpg](doc/img/32-do-monit.jpg)

---

## 4. Logging

![Server logging - image](doc/img/40-sentry.png)

+++

![Server logging - image](doc/img/42-sentry-issues.png)

+++

![`sentry.io` projects](doc/img/41-sentry-projects.png)

+++

![`sentry.io` versions](doc/img/43-sentry-version.png)

+++

![`sentry.io` mail alert](doc/img/44-sentry-mail.jpg)

---

## 5. cronjob

Each days @ 0305, `cron` runs the DB syncronisation :

```shell
user@ocp10:~$ crontab -l
5  3  *  *  * user /home/user/ocp10-django-dbsync.sh
```
```shell
user@ocp10:~$ cat ocp10-django-dbsync.sh
#!/bin/bash
# cp10-django-dbsync.sh :
# Runs a Django DB synchronization

export DJANGO_SETTINGS_MODULE='omega.settings.production'
source /home/user/ocp8/.venv/bin/activate
python3 /home/user/ocp8/manage.py prod
```
+++

![`cronjob` update log](doc/img/52-cronjob.jpg)

---

## Future…

* setting auto-deploy for production `[#68]`
* improving cronjob tests `[#65]`
* improving cronjob `[#44]`

---

### Thank you for your attention.

# (-;

# Project Title

An analytics dashboard to visualise Extinction Rebellion's UK Outcomes

## Overview

The dashboard is a Django webapp using Bokeh for visualisation.

It is hosted on Heroku

## Running Locally

Prerequisites: Python3, virtualenv, pip, Postgres, Django, Heroku

1. Clone this repo

2. Set up a virtualenv
```
$ cd xr-outcomes-dashboard
$ virtualenv ~/venvs/xr-outcomes-dashboard
$ source ~/venvs/xr-outcomes-dashboard/bin/activate
$ pip install -r requirements.txt
```

3. Config

Create a .env file based on the contents of config/settings/env.example

4. Database

Set up Postgres to run locally on your machine.

To set Postgres to start automatically: `brew services start postgresql`

Create a database and user and add the credentials to the DATABASE_URL parameter in the .env file

5. Migrations

Run
```
$ python manage.py migrate
```

6. Spin up the Django webapp
```
$ python manage.py runserver
```

7. Get the data

There is a separate Python app, https://github.com/brianspurling/xr-outcomes-pipeline, that will generate the CSV data files

In addition, you need to create the necessary commentary entries in the Django CMS:
- Create a superuser (`python manage.py createsuperuser`)
- Log in http://localhost:8000/admin

8. Check the front end

http://localhost:8000/

## Deploying Changes To Staging

1. Ask to be added as a contributor to the staging Heroku

2. Add the staging Heroku as a remote repo

```
$ heroku git:remote -a xr-outcomes-dashboard-stage
$ git remote rename heroku heroku-stage
```

3. Deploy new code to staging:
```
$ git push heroku-stage [wip-branch:]master
```

## Built With

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/) - Web framework
* [Bokeh](https://docs.bokeh.org/en/latest/index.html#) - For data visualisation
* [Pandas](https://pandas.pydata.org/) - For data processing

## License

TBD

## Acknowledgments

TBD

# KSL Scraper

[![Build Status](https://travis-ci.org/Hall-Erik/ksl-scraper.svg?branch=master)](https://travis-ci.org/Hall-Erik/ksl-scraper)
[![Coverage Status](https://coveralls.io/repos/github/Hall-Erik/ksl-scraper/badge.svg?branch=master)](https://coveralls.io/github/Hall-Erik/ksl-scraper?branch=master)

A Django/Angular app for scraping and viewing job listings found on KSL classieds, but ordered by date posted.

This is deployed on Heroku [here](https://ksl-jobs.herokuapp.com/).

## Development server

### Backend

Open a terminal in the project root and run `pip install -r requirements.txt` to download dependencies.

Run `python manage.py migrate` to build a SQLite database.

<!-- You will need a Sendgrid account to get the email backend working. Follow directons on their website to get an api key for sending mail via SMTP and set environment variables for `SENDGRID_USER` and `SENDGRID_PASS`. -->

Run `python manage.py runserver` for a dev server. The app will automatically reload if you change any of the source files.

### Frontend

Open a terminal in the ng-frontend directory and run `npm install`

Run `npm start` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Docker Compose

Alternatively, you could just run the project in Docker.

Open a terminal in the project root and run `docker-compose build` to set up your containers.

Run `docker-compose up` to run the images.

Go to `http://localhost:1337/` in your browser.

## Running unit tests

Run `python manage.py test` to execute the tests.

## Building the Frontend

The build process uses a Python script called `ng2django`.  So, be sure to use an environment where you have installed dependencies with `pip install -r requirements.txt`.

Then you can `cd` into the `ng-frontend` directory.  Run `npm run build`.

## What I learned

* Beautifulsoup for web scraping
* Angular Material for the front end
* Django for web development
* Unit testing in Django
* CI/CD with Travis-ci, Heroku and GitHub
* Test coverage reporting with Coverage<span>.</span>py and Coveralls
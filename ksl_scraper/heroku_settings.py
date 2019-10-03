from .settings import *
import django_heroku

DOMAIN = 'http://ksl-jobs.herokuapp.com'

django_heroku.settings(locals())
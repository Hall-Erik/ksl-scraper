from .settings import *
import django_heroku

DOMAIN = 'http://ksl-jobs.herokuapp.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

django_heroku.settings(locals())
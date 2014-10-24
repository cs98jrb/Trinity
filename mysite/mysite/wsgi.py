"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
activate_this = '/var/www/django/mysite/trinity/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))


import os
import sys

sys.path.append('/var/www/django/mysite/')
sys.path.append('/var/www/django/mysite/mysite/')


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

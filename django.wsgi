import os
import sys

sys.path.append("/home/deploy/apps/mlds/current")
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_mlds.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

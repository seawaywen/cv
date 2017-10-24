import os
import sys

import django
from django.core.wsgi import get_wsgi_application


django.setup()

curdir = os.path.abspath(os.path.dirname(__file__))
if curdir not in sys.path:
    sys.path.append(curdir)


import paths
paths.setup_paths()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

application = get_wsgi_application()

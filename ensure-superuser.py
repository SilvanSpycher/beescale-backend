import os
import sys

import django

# Make sure the project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

django.setup()

from django.conf import settings  # noqa: E402
from django.contrib.auth.models import User  # noqa: E402

ENV = settings.ENV

username = ENV.SUPERUSER.USERNAME
password = ENV.SUPERUSER.PASSWORD
project_name = ENV.PROJECT_NAME
email = f'webdev+{project_name}@smartfactory.ch'

if not any([username, password, project_name]):
    print('ERROR: No username/password/project_name specified.')
    sys.exit()

if User.objects.filter(username=username).count() == 0:
    User.objects.create_superuser(username, email, password)
    print('Superuser created.')
else:
    print('Superuser creation skipped.')

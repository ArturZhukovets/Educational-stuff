"""
WSGI config for configuration project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


# dotenv.load_dotenv(".env.dev")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')

application = get_wsgi_application()

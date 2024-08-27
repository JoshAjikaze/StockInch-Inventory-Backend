# inventory_app/wsgi.py
import os
import sys
from django.core.wsgi import get_wsgi_application

print("Setting DJANGO_SETTINGS_MODULE")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_app.settings')

try:
    print("Getting WSGI application")
    application = get_wsgi_application()
    print("WSGI application loaded")
except Exception as e:
    print(f"Error loading WSGI application: {e}", file=sys.stderr)
    raise

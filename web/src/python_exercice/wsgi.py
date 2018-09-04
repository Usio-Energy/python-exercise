"""
.. module:: python_exercice.wsgi
   :synopsis: The WSGI application for this project, its passed to Gunicorn
"""

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

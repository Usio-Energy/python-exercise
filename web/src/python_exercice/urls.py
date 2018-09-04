"""
.. module:: python_exercice.urls
   :synopsis: Root URL patterns.
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.views.generic import TemplateView


urlpatterns = []

# Development URL Patterns Only - For example 404 / 500 Page Previews
if settings.DEBUG:
    urlpatterns += [
        path('404/', TemplateView.as_view(template_name="404.html")),
        path('500/', TemplateView.as_view(template_name="500.html")),
    ]

urlpatterns += [
    url(r'^admin/', admin.site.urls),
]
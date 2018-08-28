from django.urls import path
from .viewsets import EntryViewSet, GetLegacyExchangeRates
from rest_framework_swagger.views import get_swagger_view

swagger = get_swagger_view('Exchange Rate API')

urlpatterns = [
    path('docs/', swagger),
    path('entries/<str:date>/', EntryViewSet.as_view({'get': 'retrieve'})),
    path('entries/update_legacy', GetLegacyExchangeRates.as_view())
]

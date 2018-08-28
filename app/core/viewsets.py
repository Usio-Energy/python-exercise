from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from .serializers import EntrySerializer, LegacySerializer
from .models import Entry


class GetLegacyExchangeRates(GenericAPIView):
    """
    Retrieve legacy data from fixer.io between two dates.

    Note that the difference between the start and end dates must be 30 days or less. The longer the window, the longer
    it will take to run. This serializer doesn't return a response, it just creates ExchangeRate objects in the DB

    **start_date:** must be in the format YYYY-MM-DD

    **end_date:** this is optional and defaults to today's date if not provided

    """
    serializer_class = LegacySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.retrieve(serializer.validated_data)
        return Response('OK', status=204)


class EntryViewSet(ModelViewSet):
    """
    Returns exchange rates for a specific date.

    **Date must be entered in the form YYYY-MM-DD**
    """
    serializer_class = EntrySerializer
    queryset = Entry.objects.all()

    def get_object(self):
        try:
            date_string = self.kwargs['date']
            return Entry.objects.get(date=date_string)
        except ObjectDoesNotExist:
            raise NotFound('No exchange rate information is available for this date')

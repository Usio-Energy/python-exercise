from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.fields import DateField
from rest_framework.exceptions import ValidationError
from .models import Entry, ExchangeRate
from datetime import timedelta


class ExchangeRateSerializer(ModelSerializer):
    class Meta:
        model = ExchangeRate
        exclude = 'id', 'entry'


class EntrySerializer(ModelSerializer):
    rates = ExchangeRateSerializer(many=True)

    class Meta:
        model = Entry
        fields = 'date', 'base', 'rates'


class LegacySerializer(Serializer):
    """
    This serializer takes a start_date and optional end_date as inputs, and calls Entry.objects.retrieve_legacy()
    """
    start_date = DateField()
    end_date = DateField(required=False)

    def validate(self, attrs):
        """
        Check that if end_date is supplied, it is later than the start date, but not by more than 30 days (as this
        would take ages to poll)
        """
        start_date = attrs['start_date']
        end_date = attrs.get('end_date')

        if end_date:
            if start_date > end_date:
                raise ValidationError('Start date must be before end date')

            diff = end_date - start_date
            if diff > timedelta(days=30):
                raise ValidationError('Cannot poll data over a period greater than 30 days')

        return super(LegacySerializer, self).validate(attrs)

    def retrieve(self, validated_data):
        Entry.objects.retrieve_legacy(**validated_data)

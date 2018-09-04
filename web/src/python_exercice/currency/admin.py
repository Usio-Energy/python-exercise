from django.contrib import admin

from .models import CurrencyRate


class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'currency_name', 'currency_base_name', 'date',]
    list_filter = ['currency_name',]
    readonly_fields = ['currency_name', 'currency_base_name', 'rate', 'date', ]

admin.site.register(CurrencyRate, CurrencyRateAdmin)

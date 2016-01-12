from pydblite import Base
from decimal import *

class Converter:
    def __init__(self, rates):
        self.__rates = rates

    def convert(self, origin_currency, target_currency, value):
        """ Persist a currency's exchange rate. """
        euro_to_origin_currency_rate = self.__rates.getRate(origin_currency) if origin_currency != 'EUR' else '1.00'
        euro_to_target_currency_rate = self.__rates.getRate(target_currency) if target_currency != 'EUR' else '1.00'

        if euro_to_origin_currency_rate is None:
            raise ValueError("Origin currency %s is not supported" % origin_currency)

        if euro_to_target_currency_rate is None:
            raise ValueError("Target currency %s is not supported" % target_currency)

        return Decimal(value) * Decimal(euro_to_target_currency_rate) / Decimal(euro_to_origin_currency_rate)

    def convert_and_round(self, origin_currency, target_currency, value):
        return self.convert(origin_currency, target_currency, value).quantize(Decimal('1.00'))



from pydblite import Base
from decimal import *

class Converter:
    def __init__(self, rates):
        self.__rates = rates

    def convert(self, origin_currency, target_currency, value):
        """ Perform conversion of a value from origin_currency to target_currency.
            Return a full-precision Decimal in case of success or raise a ValueError if any of the currencies is not known.
        """
        euro_to_origin_currency_rate = self.__rates.getRate(origin_currency) if origin_currency != 'EUR' else '1.00'
        euro_to_target_currency_rate = self.__rates.getRate(target_currency) if target_currency != 'EUR' else '1.00'

        if euro_to_origin_currency_rate is None:
            raise ValueError("Origin currency %s is not supported" % origin_currency)

        if euro_to_target_currency_rate is None:
            raise ValueError("Target currency %s is not supported" % target_currency)

        return Decimal(value) * Decimal(euro_to_target_currency_rate) / Decimal(euro_to_origin_currency_rate)

    def convert_and_round(self, origin_currency, target_currency, value):
        """ Perform conversion of a value from origin_currency to target_currency.
            Return a Decimal rounded to two decimals in case of success or raise a ValueError if any of the currencies is not known.
        """
        return self.convert(origin_currency, target_currency, value).quantize(Decimal('1.00'))



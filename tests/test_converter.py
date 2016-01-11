import unittest
import os
import codecs
from rates.converter import Converter
from rates.rates import Rates
from decimal import *

class ConverterTests(unittest.TestCase):
    def setUp(self):
        # Open non-persisted db
        repository = Rates(':memory:', True)

        # Pre-register some exchange rates
        self.__knownRates = [('PSD', 2.0), ('USD', 1.6), ('RUB', 1.9), ('TRY', 0.725)]
        for (currency, rate) in self.__knownRates:
            repository.setRate(currency, rate)

        self.__converter = Converter(repository)

    def test_someConversions(self):
        asserts = [('RUB', 'TRY', '4.85', '1.85'), \
                   ('EUR', 'USD', '3.70', '5.92'), \
                   ('TRY', 'TRY', '0.45', '0.45'), \
                   ('EUR', 'EUR', '4.85', '4.85'), \
                   ('PSD', 'USD', '0.00', '0.00'), \
                   ('TRY', 'EUR', '7.87', '10.86'), \
                  ]

        for (fromCurrency, toCurrency, value, expectedValue) in asserts:
            self.assertEqual(self.__converter.convert_and_round(fromCurrency, toCurrency, Decimal(value)), Decimal(expectedValue))

    def test_someInvalidConversions(self):
        asserts = [('RUB', 'CCC'), \
                   ('CCC', 'USD'), \
                   ('CCC', 'CCC'), \
                  ]

        for (fromCurrency, toCurrency) in asserts:
            self.assertRaises(ValueError, self.__converter.convert_and_round, fromCurrency, toCurrency, Decimal('1.00'))

    def test_idempotency(self):
        for value in list(map(Decimal, ['1246.87', '0.15', '875.00', '122.36', '0.01'])):
            for (from_currency, _) in self.__knownRates:
                for (to_currency, _) in self.__knownRates:
                    converted_value = self.__converter.convert(to_currency, from_currency, value)
                    idempotent_value = self.__converter.convert_and_round(from_currency, to_currency, converted_value)
                    self.assertEqual(idempotent_value, value)
import unittest
from rates.rates import Rates

class RatesTests(unittest.TestCase):
    def setUp(self):
        # Open non-persisted db
        self.__repository = Rates(':memory:', True)

        # Pre-register some exchange rates
        self.__knownRates = [('PSD', 2.0), ('USD', 1.6), ('RUB', 1.9), ('TRY', 0.7)]
        for (currency, rate) in self.__knownRates:
            self.__repository.setRate(currency, rate)

    def test_setNewRate(self):
        self.assertEqual(self.__repository.getRatesCount(), 4)
        self.__repository.setRate('RRR', 0.5)
        self.assertEqual(self.__repository.getRatesCount(), 5)

    def test_setInvalidRate(self):
        self.assertRaises(AssertionError, self.__repository.setRate, 'RRR', -0.5)
        self.assertRaises(AssertionError, self.__repository.setRate, 'RRR', 0.0)
        self.assertRaises(AssertionError, self.__repository.setRate, 'RRR', -0.0)

    def test_setExistingRate(self):
        self.assertEqual(self.__repository.getRatesCount(), 4)
        self.assertEqual(self.__repository.getRate('PSD'), 2.0)
        self.__repository.setRate('PSD', 0.1)
        self.assertEqual(self.__repository.getRatesCount(), 4)
        self.assertEqual(self.__repository.getRate('PSD'), 0.1)

    def test_getExistingRate(self):
        self.assertEqual(self.__repository.getRate('USD'), 1.6)

    def test_getUnknownRate(self):
        self.assertEqual(self.__repository.getRate('FYL'), None)

    def test_getAllRates(self):
        self.assertEqual(self.__repository.getAllRates(), self.__knownRates)
import server
import unittest
from rates.rates import Rates
from rates.converter import Converter
import json

class ServerTests(unittest.TestCase):

    def setUp(self):
        server.server.config['TESTING'] = True
        self.app = server.server.test_client()
        rates = Rates(':memory:', True)
        server.converter = Converter(rates)
        rates.setRate('USD', 1.45)
        rates.setRate('TYR', 0.723)
        rates.setRate('KD', 1.45)
        rates.setRate('RTATATTATATA', 1.45)

    def queryAndAssert(self, query, expected_status, expected_answer):
        parameters = ('?query=%s' % query) if query is not None else ''
        response = self.app.get('/money/convert' + parameters)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('answer', data)
        self.assertEqual(len(data), 1)
        self.assertIsInstance(data['answer'], str)
        self.assertEqual((response.status, data['answer']), (expected_status, expected_answer))

    def test_workingQuery(self):
        self.queryAndAssert('9.95 USD en TYR', '200 OK', '9.95 USD = 4.96 TYR')

    def test_workingQuery_WidthoutDecimal(self):
        self.queryAndAssert('995 USD en TYR', '200 OK', '995 USD = 496.13 TYR')

    def test_workingQuery_WithSpaces(self):
        self.queryAndAssert('   995  USD    en  TYR      ', '200 OK', '995 USD = 496.13 TYR')

    def test_workingQuery_LowerCaseCurrency(self):
        self.queryAndAssert('995 usd en tYr', '200 OK', '995 USD = 496.13 TYR')

    def test_failingQuery_NullOrEmptyQuery(self):
        self.queryAndAssert('', '500 UnknownError', "I' sorry Dave. I'm afraid. I can't do that")
        self.queryAndAssert(None, '500 UnknownError', "I' sorry Dave. I'm afraid. I can't do that")

    def test_failingQuery_PlainWrongQuery(self):
        self.queryAndAssert('fzeikfms6513fzef', '500 UnknownError', "I' sorry Dave. I'm afraid. I can't do that")
        self.queryAndAssert('00000 en 00000', '500 UnknownError', "I' sorry Dave. I'm afraid. I can't do that")

    def test_failingQuery_UnknownCurrencies(self):
        self.queryAndAssert('995 RRR en TYR', '500 UnknownError', "I' sorry Dave. I'm afraid. I can't do that")
        self.queryAndAssert('995 USD en RRR', '500 UnknownError', "I' sorry Dave. I'm afraid. I can't do that")
        self.queryAndAssert('995 RRR en RRR', '500 UnknownError', "I' sorry Dave. I'm afraid. I can't do that")

    def test_failingQuery_MalformedValue(self):
        self.queryAndAssert('.995 USD en TYR', '500 UnknownError', "I' sorry Dave. I'm afraid. I can't do that")
        self.queryAndAssert('1.78.3 USD en TYR', '500 UnknownError', "I' sorry Dave. I'm afraid. I can't do that")
        self.queryAndAssert('-0.4995 USD en TYR', '500 UnknownError', "I' sorry Dave. I'm afraid. I can't do that")
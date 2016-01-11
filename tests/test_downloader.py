import unittest
import os
import rates.downloader

class DownloaderTests(unittest.TestCase):
    def test_sample(self):
        result = dict(rates.downloader.getExchangeRates(os.path.join(os.path.dirname(__file__), 'exchange_rate_sample.xml')))
        self.assertEqual(result, {'USD': 1.0888, 'JPY': 128.33, 'BGN': 1.9558})


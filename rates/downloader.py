from urllib.request import urlopen
from xml.etree import ElementTree
import re

def getExchangeRates(url = None):
    """ Read and parse an xml file provided as a stream and return a stream of (currency, rate) tuples.
        If no input stream is provided, the default one provided by defaultDownloader() is used.
    """
    ns = {'def': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}

    root = ElementTree.parse(url if url is not None else defaultDownloader()).getroot()
    for entry in root.findall('def:Cube/def:Cube/def:Cube', ns):
        currency = entry.get('currency').upper()
        if re.match('^[A-Z]+$', currency):
            try:
                yield currency, float(entry.get('rate'))
            except ValueError:
                pass # silently ignore invalid currency rate that could occur

def defaultDownloader():
    return urlopen('http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')


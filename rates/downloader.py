from urllib.request import urlopen
from xml.etree import ElementTree

def getExchangeRates(url = None):
    ns = {'def': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}

    root = ElementTree.parse(url if url is not None else defaultDownloader()).getroot()
    for entry in root.findall('def:Cube/def:Cube/def:Cube', ns):
        yield entry.get('currency'), float(entry.get('rate'))

def defaultDownloader():
    return urlopen('http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')


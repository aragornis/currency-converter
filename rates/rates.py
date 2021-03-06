from pydblite import Base

class Rates:
    """ Persistence layer for exchange rates. """

    def __init__(self, filename, erase_db):
        self.__db = Base(filename)
        self.__db.create('currency', 'rate', mode="override" if erase_db else "open")
        self.__db.create_index('currency')

    def setRate(self, currency, rate):
        """ Persist a currency's exchange rate. """
        assert rate > 0.0

        records = self.__db._currency[currency]

        if len(records) > 0:
            assert len(records) == 1 # We never expect several exchange rates for the same currency
            self.__db.update(records[0], rate = rate)
        else:
            self.__db.insert(currency = currency, rate = rate)

        self.__db.commit()

    def getRate(self, currency):
        """ Get the exchange rate with EUR for the provided currency or None if it is not found.
            An exchange rate for currency CUR is Value(EUR) / Value(CUR): 1 EUR = rate(CUR) CUR <=> 1/rate(CUR) EUR = 1 CUR.
        """
        records = self.__db._currency[currency]
        return records[0]['rate'] if len(records) > 0 else None

    def getAllRates(self):
        """ Get all known exchange rates as a dict. """
        return [(r['currency'], r['rate']) for r in self.__db]

    def getRatesCount(self):
        """ Get total number of exchange rates in db. """
        return len(self.__db)
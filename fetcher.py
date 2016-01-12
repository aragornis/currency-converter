from rates.rates import Rates
from rates import downloader
import sys

if __name__ == "__main__":
    # Parse arguments
    db_file = sys.argv[1] if len(sys.argv) > 1 else "rates.pdl"

    # Download and store rates
    rates = Rates(db_file, True)
    for (currency, rate) in downloader.getExchangeRates():
        print("Set exchange rate %s for 'EUR' -> '%s'" % (rate, currency))
        rates.setRate(currency, rate)

    print("%s exchange rates have been retrieved and saved to %s" % (rates.getRatesCount(), db_file))
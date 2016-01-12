from flask import Flask
from flask import jsonify
from flask import request
from rates.rates import Rates
from rates.converter import Converter
from decimal import *
import sys
import re

server = Flask(__name__)

def parse_query(query):
    """ Parse received query and return tuple of currencies and value or None if the input is malformed. """
    if query is not None:
        match = re.match('^\s*(\d+(\\.\d+)?)\s+([a-zA-Z]+)\s+en\s+([a-zA-Z]+)\s*$', query)
        if match:
            return (Decimal(match.group(1)), match.group(3).upper(), match.group(4).upper())

@server.route("/money/convert", methods=['GET'])
def convert():
    """ Perform conversion of a value from one currency to another. """

    query = parse_query(request.args.get('query', None))

    if not query:
        return make_error_response()

    value, origin_currency, target_currency = query

    try:
        converted_value = converter.convert_and_round(origin_currency, target_currency, value)
    except:
        return make_error_response()

    result = '%s %s = %s %s' % (value, origin_currency, converted_value, target_currency)
    return jsonify(answer = result)

def make_error_response():
    return jsonify(answer = "I' sorry Dave. I'm afraid. I can't do that"), '500 UnknownError'

if __name__ == "__main__":
     # Parse arguments
    db_file = sys.argv[1] if len(sys.argv) > 1 else "rates.pdl"
    debug = '--debug' in sys.argv

    # Load data from db
    rates = Rates(db_file, False)
    print("%s exchange rates loaded from %s" % (rates.getRatesCount(), db_file))

    # Create converter service
    converter = Converter(rates)

    # Start server
    server.run(debug=True)
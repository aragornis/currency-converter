# currency-converter

## CLI
```
python fetcher.py [db_file] # Fetches exchange rate from the internet and store them in provided file
python server.py [db_file [--debug]] # Start REST server
```

## How to run tests

```
python -m unittest discover
```

## How to run - using Python 3.5

```
pip install -r requirements.txt
python fetcher.py rates.pdl
python server.py rates.pdl
```

## TODO

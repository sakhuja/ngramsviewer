### 1. Generate indexes from the books dataset

USAGE   : `./ngrams.py --year <YEAR> --gram <GRAMS> [--withdocids] [--withfreq] [--debug]`
USAGE   : `./ngrams.py --help`

EXAMPLE 1: `./ngrams.py --year 2012 --gram 4 --withfreq # this would generate the freq count index for the ngrams`
EXAMPLE 2: `./ngrams.py --year 2012 --gram 4 --withdocids # this would generate the docids based index for the ngrams`


### OR, Renerate the complete n-grams dataset, using this
`./scripts/generate-ngrams.sh`
    
### 2. run the ngram viz app
`source ${BASE_PATH}/venvs/ngramenv/bin/activate`
`python manage.py runserver`
`http://127.0.0.1:5000/ngrams/viz`

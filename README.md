### 1. Generate indexes from the books dataset

**USAGE** : `./ngrams.py --year <YEAR> --gram <GRAMS> [--withdocids] [--withfreq] [--debug]`

**USAGE** : `./ngrams.py --help`

**EXAMPLE 1:** `./ngrams.py --year 2012 --gram 4 --withfreq # this would generate the freq count index for the ngrams`
**EXAMPLE 2:** `./ngrams.py --year 2012 --gram 4 --withdocids # this would generate the docids based index for the ngrams`

### **OR**, Renerate the complete n-grams dataset, using this
`./scripts/generate-ngrams.sh`
    
### 2. Run the ngram viz app
`source ${BASE_PATH}/venvs/ngramenv/bin/activate`
`python manage.py runserver`
`http://127.0.0.1:5000/ngrams/viz`

### 3. remote hosting
`http://peaceful-tor-45189.herokuapp.com/ngrams/viz`
----------------------------------------------------

####  Sample Queries :

### 5-Grams : Sample Queries

### 4-Grams : Sample Queries
if they did not

### 3-Grams : Sample Queries
    and so on
    
### 2-Grams : Sample Queries
this is, to be

### 1-Grams : Sample Queries
who, when, where
girl, woman, lady
man, gentleman

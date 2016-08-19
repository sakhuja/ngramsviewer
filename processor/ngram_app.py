import os

from flask import render_template, request, url_for

from processor import main_app
from processor.forms import gramsForm
from flask import redirect


@main_app.route('/ngrams/viz', methods=['GET', 'POST'])
def ngram_viz():

    form = gramsForm(request.form)
    if request.method == 'POST' and form.validate():
        phrases = form.phrases.data.strip()
        phrases_lst = phrases.split(",")
        phrases_processed = []

        for phrase in phrases_lst:
            phrases_processed.append(phrase.strip(" "))

        search_index(phrases_processed)
        return redirect(url_for('ngram_viz'))

    elif request.method == 'GET':
        return render_template('viz/vizgrams.html', form=form)


def read_from_corpus_index(n, phrase, d):
    cwd = os.getcwd()
    root = cwd + "/datasets/ngrams/withfreq"

    try:
        for f in os.listdir(os.path.join(root)):
            fn = os.path.join(root, f)
            if f.startswith(str(n) + "gram."):
                yr = f.split('.')[1]

                d[yr] = d.get(yr, {})

                with open(fn, 'r') as fl:
                    for line in fl:
                        try:
                            ngram, freq = line.split('`')
                        except ValueError as err:
                            print err.message
                            continue
                        if phrase == ngram:
                            # d[yr].add(ngram)
                            d[yr][ngram] = d[yr].get(ngram, 0)
                            d[yr][ngram] += int(freq.strip('\n'))

    except (RuntimeError, TypeError, NameError, ) as err:
        print err.message

    return d


def generate_viz_data(d):
    """
    This is the file that actually writes to the

    :param d:
    :return:
    """
    cwd = os.getcwd()
    fn = cwd + "/processor/static/data/corpus.csv"
    header_flg = True

    try:
        with open(fn, 'w') as fl:
            for year, body in d.iteritems():
                grams = []
                freqs = []
                for gram, freq in body.iteritems():
                    grams.append(gram)
                    freqs.append(str(freq))

                if header_flg and len(grams) > 0:
                    fl.write("Date" + "," + ','.join(grams) + "\n")
                    header_flg = False

                if len(freqs) > 0:
                    fl.write(year + "," + ','.join(freqs) + "\n")

    except (RuntimeError, TypeError, NameError) as err:
        print err


def search_index(phrases_lst):
    """
    This should load the relevant ngram index
    file in memory, search agaainst it the
    queried phrase and update the corpus.csv

    :param phrases_lst: list of n-grams to search on.
    """
    try:
        print phrases_lst
        d = dict()

        for phrase in phrases_lst:
            n = len(phrase.split(" "))
            assert 0 < n < 6
            d = read_from_corpus_index(n, phrase, d)

        generate_viz_data(d)

    except IOError as e:
        print e.strerror


@main_app.route('/phrase', methods=['GET', 'POST'])
def filter_grams():
    form = gramsForm(request.form)
    if request.method == 'POST' and form.validate():
        phrases = form.phrases.data.strip()
        phrases_lst = phrases.split(",")
        phrases_processed = []

        for phrase in phrases_lst:
            phrases_processed.append(phrase.strip(" "))

        search_index(phrases_processed)
        return redirect(url_for('ngram_viz'))

    if request.method == 'GET':
        return render_template('viz/phraseform.html', form=form)


@main_app.route('/')
def hello():
    print "hello ngrams"

#!/usr/bin/env python

import argparse
import os
import consts


def word_split(text):
    """
    Split a text in words. Returns a list of tuple that contains
    (word, location) location is the starting byte position of the word.
    """
    word_list = []
    wcurrent = []
    windex = None

    for i, c in enumerate(text):
        if c.isalnum():
            wcurrent.append(c)
            windex = i
        elif wcurrent:
            word = u''.join(wcurrent)
            word_list.append((windex - len(word) + 1, word))
            wcurrent = []

    if wcurrent:
        word = u''.join(wcurrent)
        word_list.append((windex - len(word) + 1, word))

    return word_list


def tokenize_text(text, window_size):
    """
    Split the book into words with space as the delimiter.
    return (word, location), where location is the position
    of the word in the text.
    """
    window_size = int(window_size)
    phrase = []
    phrase_list = []
    text = text.replace('\r\n', ' ')
    words = text.split(' ')
    word_pos = -1
    within_phrase_pos = -1
    pause_word_pos = False

    # for word in words:
    # more_words = word.split('\r\n')
    # for more_word in more_words:
    while (word_pos + window_size) < len(words):
        if len(phrase) < (window_size):
            within_phrase_pos += 1
            phrase.append(words[within_phrase_pos])
        else:
             phrase_list.append((' '.join(phrase), word_pos))
             pause_word_pos = False
             phrase = []
             word_pos += 1
             within_phrase_pos = word_pos

    # print phrase_list
    return phrase_list


def words_cleanup(words):
    """
    Remove words with length less then a minimum and stopwords.
    """
    cleaned_words = []
    for word, index in words:
        if len(word) < consts._WORD_MIN_LENGTH or word in consts._STOP_WORDS:
            continue

        if word.isdigit():
            continue

        cleaned_words.append((index, word))
    return cleaned_words


def words_normalize(words):
    """
    Do a normalization precess on words. In this case is just a tolower(),
    but you can add accents stripping, convert to singular and so on...
    """
    normalized_words = []
    for index, word in words:
        wnormalized = word.lower()
        normalized_words.append((index, wnormalized))
    return normalized_words


def word_index(text, grams):
    """
    Just a helper method to process a text.
    It calls word split, normalize and cleanup.
    """
    words_and_pos = tokenize_text(text, grams)
    # words = words_normalize(words)
    # words = words_cleanup(words)
    return words_and_pos


def inverted_index(text, gram):
    """
    Create an Inverted-Index of the specified text document.
        {word:[locations]}
    """
    inverted = {}

    for word, index in word_index(text, gram):
        locations = inverted.setdefault(word, [])
        locations.append(index)

    return inverted


def inverted_index_add(inverted, doc_id, doc_index):
    """
    Add Invertd-Index doc_index of the document doc_id to the
    Multi-Document Inverted-Index (inverted),
    using doc_id as document identifier.
        {word:{doc_id:[locations]}}
        :param doc_index:
        :param doc_id:
        :param inverted:
    """
    for word, locations in doc_index.iteritems():
        indices = inverted.setdefault(word, {})
        indices[doc_id] = locations
    return inverted


def search(inverted, query):
    """
    Returns a set of documents id that contains all the words in your query.
    :param query:
    :param inverted:
    """
    words = [word for _, word in word_index(query) if word in inverted]
    results = [set(inverted[word].keys()) for word in words]
    return reduce(lambda x, y: x & y, results) if results else []


if __name__ == '__main__':
    documents = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", help="year")
    parser.add_argument("-g", "--gram", help="specify how many grams")
    parser.add_argument("-d", "--debug", help="debug mode on", dest='debug', action='store_true')
    parser.add_argument("-w", "--withdocids", help="with doc ids", dest='withdocids', action='store_true')
    parser.add_argument("-f", "--withfreq", help="with token freq", dest='withfreq', action='store_true')

    args = parser.parse_args()
    if args.debug:
        print "[ DEBUG ] args.gram ---> " + args.gram
        print "[ DEBUG ] args.year ---> " + args.year
        print "[ DEBUG ] args.debug ---> " + str(args.debug)
        print "[ DEBUG ] args.withfreq ---> " + str(args.withfreq)
        print "[ DEBUG ] args.withdocids ---> " + str(args.withdocids)

    cwd = "/Users/aditya.sakhuja/Code/ngramer"
    print "cwd : " + cwd
    root = cwd + "/datasets/corpus"
    year = args.year
    if args.debug:
        print "[ DEBUG ] ---> " + os.path.join(root, year)

    for f in os.listdir(os.path.join(root, year)):
        if args.debug:
            print "[ DEBUG ] ---> " + os.path.join(root, year, f)

        cf = open(os.path.join(root, year, f), 'r')
        d = cf.read()
        key = f + "_" + year
        if args.debug:
            print key

        documents[key] = d

    # Build Inverted-Index for documents
    inverted = {}
    for doc_id, text in documents.iteritems():
        doc_index = inverted_index(text, args.gram)
        inverted_index_add(inverted, doc_id, doc_index)

    # Print Inverted-Index
    for phrase, doc_locations in inverted.iteritems():
        if args.withdocids:
            print phrase, doc_locations

        if args.withfreq:
            total_count = 0
            for docname, positions in doc_locations.iteritems():
                total_count += len(positions)
            print phrase + "`" + str(len(positions))

    exit(1)

    # Search something and print results
    queries = ['West Bank']
    for query in queries:
        result_docs = search(inverted, query)
        print "Search for '%s': %r" % (query, result_docs)
        for _, word in word_index(query):
            def extract_text(doc, index):
                return documents[doc][index:index + 20].replace('\n', ' ')
            for doc in result_docs:
                for index in inverted[word][doc]:
                    print '   - %s...' % extract_text(doc, index)
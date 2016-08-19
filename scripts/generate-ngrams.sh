#!/usr/bin/env bash

CODE_HOME="/Users/aditya.sakhuja/Code"
BASE_PATH=${CODE_HOME}"/ngramer/datasets/ngrams/withfreq/"
YRS="2012 2013 2014 2015 2016"

for YR in ${YRS}
do
    ./ngrams.py --gram 1 --year ${YR} --withfreq | sort -t"\`" -k 1 > ${BASE_PATH}/1gram.${YR}.csv
    ./ngrams.py --gram 2 --year ${YR} --withfreq | sort -t"\`" -k 1 > ${BASE_PATH}/2gram.${YR}.csv
    ./ngrams.py --gram 3 --year ${YR} --withfreq | sort -t"\`" -k 1 > ${BASE_PATH}/3gram.${YR}.csv
    ./ngrams.py --gram 4 --year ${YR} --withfreq | sort -t"\`" -k 1 > ${BASE_PATH}/4gram.${YR}.csv
    ./ngrams.py --gram 5 --year ${YR} --withfreq | sort -t"\`" -k 1 > ${BASE_PATH}/5gram.${YR}.csv
    echo ${YR}" done."
done

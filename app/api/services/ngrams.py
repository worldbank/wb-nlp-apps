import pandas as pd
import multiprocessing as mp
import os
import pickle


class NGramMapper:
    def __init__(self, whitelist_file, cleaner=None):
        # cleaner = None
        # Headers `ngram`, `cleaned`

        self.whitelist_ngrams = pd.read_csv(whitelist_file, low_memory=False)
        self.ngrams_map = self.whitelist_ngrams[['ngram']]
        self.ngrams_map['source'] = self.ngrams_map.ngram.str.split('_').map(lambda x: ' '.join(x))

        self.ngrams_map = self.ngrams_map.set_index('source').to_dict()['ngram']

        for _, row in self.whitelist_ngrams.iterrows():
            self.ngrams_map[row['cleaned']] = row['ngram']

    def replace_ngrams(self, txt):
        txt = ' ' + txt + ' '
        for source in sorted(self.ngrams_map, key=lambda x: len(x.split()), reverse=True):
            txt = txt.replace(f' {source} ', f' {self.ngrams_map[source]} ')

        return txt.strip()

    def replace_ngrams_in_file(self, fname):
        with open(fname) as fl:
            txt = fl.read()

        return self.replace_ngrams(txt)

    def clean_text(self, ngram):
        return self.cleaner.clean_text(ngram)['text']

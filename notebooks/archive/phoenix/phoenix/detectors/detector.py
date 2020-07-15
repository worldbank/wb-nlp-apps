import re
import pandas as pd
import os


class Detector:
    space_aggregate = re.compile('[ ]+')

    def __init__(
        self, map_file, index_col=0,
        noise_pattern=re.compile('[^a-zA-ZÀ-ÖØ-öø-ÿ ]+')
    ):
        self.map_file = map_file
        self.noise_pattern = noise_pattern
        self.build_map(index_col=index_col)

    def build_map(self, index_col):
        '''
        Generates a map between a variant of a code into the appropriate standard code from a whitelist.
        Assume that the whitelist `map_file` is an excel file without header and the first column is the code to use.
        The `map_file` must be in UTF-8 encoding.
        '''
        map_df = pd.read_csv(self.map_file, header=None, index_col=0)
        if index_col != 0:
            map_df.index = map_df[map_df.columns[index_col - 1]]

        self.map = {}
        for ckey, clist in map_df.iterrows():
            for c in clist.dropna():
                if self.noise_pattern is not None:
                    c = self.noise_pattern.sub('', c.lower().strip())
                ckey = ckey.strip()
                self.map[c.lower()] = {'code': ckey}

    def preprocess_text(self, text):
        text = text.lower()

        # Reduce false-positive because the $ symbol is removed and the remaining us gets detected
        text = text.replace('us$', ' ')

        text = self.noise_pattern.sub(' ', text)
        text = text.replace('us dollar', ' ')
        text = self.space_aggregate.sub(' ', text)
        text = f' {text} '

        return text

    def detect_entity(self, text):
        text = self.preprocess_text(text)

        freq = {}

        for c, val in sorted(self.map.items(), key=lambda x: -len(x[0])):
            data = text

            code = val['code']
            _freq = data.count(f' {c} ')

            freq[code] = freq.get(code, 0) + _freq
            text = text.replace(c, '')

        freq = {i: j for i, j in freq.items() if j > 0}
        return freq

    def detect_from_file(self, fname, return_df=True):
        try:
            with open(fname) as fl:
                text = fl.read()
        except UnicodeDecodeError:
            with open(fname, 'rb') as fl:
                text = fl.read()
                text = str(text, 'utf-8', 'ignore')

        doc_id = os.path.basename(fname).split('.')[0]

        return_val = {doc_id: self.detect_entity(text)}

        if return_df:
            return_val = pd.DataFrame(return_val)

        return return_val
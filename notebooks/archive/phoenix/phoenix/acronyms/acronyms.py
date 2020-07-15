import re
import pandas as pd
import nltk

nltk.data.path.append("/R/nltk_data")

from nltk.corpus import stopwords
from collections import Counter
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity


acronyms_pattern = re.compile('(\([A-Z]{2,}\))')
candidates_pattern = re.compile('([A-Z][a-z]+|\([A-Z]{2,}\))')
newline_pattern = re.compile(b'[\r\n]+')
whitespaces_pattern = re.compile('\s+')
alphabet_pattern = re.compile('[A-Z-a-z]+')
stops = set(['the', 'of', 'in', 'and', 'or', 'for'])
stops.update(stopwords.words('english'))


def extract_acronyms(txt):
    acronyms = [i.strip('(').strip(')') for i in acronyms_pattern.findall(txt)]
    keyword = '|'.join([f'\({k}\)' for k in acronyms])
    candidates_acronym_pattern = "((?:[a-zA-Z'-]+ ){0,5})(" + keyword + ")" #((?:[^a-zA-Z'-]+[a-zA-Z'-]+){0,5})"
    candidates_acronym_pattern = re.compile(candidates_acronym_pattern)
    acronym_candidates_lists = candidates_acronym_pattern.findall(whitespaces_pattern.sub(' ', txt))
    detected_acronyms = {}

    for ip in acronym_candidates_lists:
        candidate, acronym = ip
        candidate = ' '.join(alphabet_pattern.findall(candidate))

        full_name = []
        formed_acronym = []
        acr = acronym.strip('(').strip(')')
        l = 0
        acr_char_counts = Counter(acr)
        for ix, c in enumerate(candidate.strip().split()[::-1]):
            c_title = c.title()
            if c in stops and l > 0:
                full_name.append(c)
            elif (c_title[0] in acr_char_counts) and (acr_char_counts[c_title[0]] > 0):
                l += 1
                full_name.append(c_title)
                formed_acronym.append(c_title)
                acr_char_counts[c_title[0]] -= 1
            if l >= len(acr):
                detected_acronyms[acr] = " ".join(full_name[::-1])
                break

    return detected_acronyms


def detect_acronyms(txt):
    '''
    This method extracts acronyms from a text document. An acronym can be detected if it's defined with similar form as follows:
        National Population and Housing Census (NPHC)
        Landscape Approach to Forest Restoration and Conservation (LAFREC)

    Input:
        text (str): string type object where acronyms will be detected from.

    Output:
        acronyms_map (dict): this is a dictionary that maps the acronym to a set of possible original forms of the acronym.

    '''

#     acronyms = acronyms_pattern.findall(txt)
#     candidates = candidates_pattern.findall(txt)

#     detected_acronyms = []

#     for a in acronyms:
#         if a in candidates:
#             ix = candidates.index(a)
#             l = len(a) - 2
#             detected_acronyms.append((a[1:-1], ' '.join(candidates[ix - l:ix])))

    detected_acronyms = extract_acronyms(txt).items()
    acronyms_map = {}

    for a, n in detected_acronyms:
        if a in acronyms_map:
            acronyms_map[a].add(n)
        else:
            acronyms_map[a] = set([n])

    return acronyms_map


def detect_acronyms_from_file(fpath):
    try:
        with open(fpath, 'rb') as fl:
            txt = fl.read()
            txt = newline_pattern.sub(b' ', txt)
            txt = txt.decode('utf-8', errors='ignore')

    except UnicodeDecodeError:
        with open(fpath, 'rb') as fl:
            txt = fl.read()
            txt = newline_pattern.sub(b' ', txt)
            txt = txt.decode('utf-8', errors='ignore')

    return detect_acronyms(txt)


def merge_corpora_acronyms_map(acronyms_maps):
    merged_corpora_acronyms_map = {}

    for acronyms_map in acronyms_maps:
        if acronyms_map:
            for a, payload in acronyms_map.items():
                doc_freq = payload['doc_freq']
                prototypes = payload['prototypes']

                if a in merged_corpora_acronyms_map:
                    for i in prototypes:
                        if i in merged_corpora_acronyms_map[a]['prototypes']:
                            merged_corpora_acronyms_map[a]['prototypes'] += prototypes[i]
                        else:
                            merged_corpora_acronyms_map[a]['prototypes'] = prototypes[i]

                    merged_corpora_acronyms_map[a]['doc_freq'] += doc_freq
                else:
                    merged_corpora_acronyms_map[a] = {'prototypes': prototypes, 'doc_freq': doc_freq}

    return merged_corpora_acronyms_map


def get_corpus_top_acronym_prototypes(corpus_full_acronyms_map, prototypes=5):
    acronyms_popular_prototype = []
    columns=['acronym', 'doc_freq', 'full_name', 'percentage']

#     for i in range(1, prototypes + 1):
#         columns.append(f'popular_prototype_{i}')
#         columns.append(f'doc_proportion_{i}')

    for a, d in corpus_full_acronyms_map.items():
        x = pd.Series(corpus_full_acronyms_map[a]['prototypes'])
        y = (x / corpus_full_acronyms_map[a]['doc_freq']).sort_values(ascending=False)
        doc_freq = corpus_full_acronyms_map[a]['doc_freq']

        for ind in range(prototypes):
            d = [a, doc_freq]
            try:
                i = y.index[ind]
                v = y[i]
            except:
                break
            d.append(i)
            d.append(v)

            acronyms_popular_prototype.append(d)

    acronyms_popular_prototype = pd.DataFrame(
        acronyms_popular_prototype,
        columns=columns
    )

    acronyms_popular_prototype = acronyms_popular_prototype.sort_values('doc_freq', ascending=False).reset_index(drop='index')

    return acronyms_popular_prototype


class AcronymMapper:
    def __init__(self, whitelist_file, sim_thresh=0.8):
        whitelist_acronyms = pd.read_csv(whitelist_file, header=None)
        self.whitelist_acronyms = whitelist_acronyms.rename(columns={0: 'acronym', 1: 'actual'})

        self.hvec = HashingVectorizer()

        # Can be in a dataframe but I don't want to stack the vectors every time we infer.
        self.acronyms = self.whitelist_acronyms.acronym.values
        self.actual = self.whitelist_acronyms.actual.values
        self.actual_vectors = self.hvec.transform(self.actual)
        self.sim_thresh = sim_thresh

    def get_valid_doc_acronym(self, txt):

        # Detect acronyms present in the document
        doc_detected_acronyms = detect_acronyms(txt)
        valid_doc_acronyms = {}
        invalid_in_doc_to_actual = {}

        for i in doc_detected_acronyms:
            c = self.whitelist_acronyms[self.whitelist_acronyms.acronym == i]

            if not c.empty:
                # For now, this assumes that there will only be one detected full name for an acronym.
                valid_candidate_acronyms = doc_detected_acronyms[i]
                assert(len(valid_candidate_acronyms) == 1)

                valid_candidate_acronyms_vec = self.hvec.transform(valid_candidate_acronyms)

                sims = cosine_similarity(self.actual_vectors, valid_candidate_acronyms_vec)
                max_index = sims.argmax()
                max_sim = sims[max_index]

                if max_sim > self.sim_thresh:
                    valid_full = self.actual[max_index]
                    valid_doc_acronyms[i] = valid_full

                    doc_full = list(valid_candidate_acronyms)[0]

                    if doc_full != valid_full:
                        invalid_in_doc_to_actual[doc_full] = valid_full

        return valid_doc_acronyms, invalid_in_doc_to_actual

    def expand_doc_acronyms(self, txt):
        valid_doc_acronyms, invalid_in_doc_to_actual = self.get_valid_doc_acronym(txt)

        for acr in valid_doc_acronyms:
            txt = txt.replace(f' ({acr})', ' ')
            txt = txt.replace(f' {acr} ', f' {valid_doc_acronyms[acr]} ')

        for invalid_full in invalid_in_doc_to_actual:
            txt = txt.replace(invalid_full, invalid_in_doc_to_actual[invalid_full])

        return txt

    def expand_doc_acronyms_in_file(self, fname):
        with open(fname) as fl:
            txt = fl.read()

        return self.expand_doc_acronyms(txt)

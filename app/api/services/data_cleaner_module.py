#!/usr/bin/env python
# coding: utf-8

# # <div style="text-align:center">World Bank Documents and Reports Cleaner</div>
#
# This notebook implements the cleaner classes for the data from the **Documents and Reports API**. This cleaner module provides respelling functionality as well.

# In[ ]:


# # Requirements:
# # Please install spacy library and the `en` model
# !~/anaconda3/bin/pip install spacy
# !~/anaconda3/bin/python -m spacy download en
# !~/anaconda3/bin/pip install contexttimer


# ### Installing pattern as alternative to pyenchant
# #### Note, the pattern module's spell checking function is quite slow!
#
#
# Clone first the development repo ([pypi version is outdated](https://github.com/clips/pattern/issues/217
# ))
# - `git clone -b development https://github.com/clips/pattern`
# - `cd pattern/`
# - Commenting out `"mysqlclient"` inside the `setup.py` file may be necessary if errors are encountered in the next step.
# - `pip install .`
#
# Make sure that the `pip` that you use corresponds to the python installation that you will use to run the notebook.

# In[1]:


from sklearn.feature_extraction import stop_words
from contexttimer import Timer
import spacy
from scipy.stats import rankdata
from nltk.metrics.distance import edit_distance
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import multiprocessing
import multiprocessing as mp
from joblib import Parallel, delayed
from langdetect import detect, detect_langs
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import PlaintextCorpusReader, wordnet
from nltk.corpus import stopwords as nltk_stopwords
from nltk.corpus import words
from services.acronyms.AcronymModule import AcronymMapper


# In[2]:


import os
import re
import numpy as np
import pandas as pd
import nltk

# Spelling correction
ENCHANT_INSTALLED = True
try:
    from enchant.checker import SpellChecker
    from enchant import Dict
except:
    # Make sure that these are installed for the pattern module to work
    for token in ("stopwords", "wordnet", "wordnet_ic", "sentiwordnet"):
        nltk.download(token)
    print('Using pattern module...')
    import pattern.en
    ENCHANT_INSTALLED = False


# In[3]:


roman_nums = set([
    'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi',
    'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx',
    'xxi', 'xxii', 'xxiii', 'xxiv', 'xxv', 'xxvi', 'xxvii', 'xxviii',
    'xxix', 'xxx', 'xxxi', 'xxxii', 'xxxiii', 'xxxiv', 'xxxv', 'xxxvi',
    'xxxvii', 'xxxviii', 'xxxix', 'xl', 'xli', 'xlii', 'xliii', 'xliv',
    'xlv', 'xlvi', 'xlvii', 'xlviii', 'xlix', 'l', 'li', 'lii', 'liii',
    'liv', 'lv', 'lvi', 'lvii', 'lviii', 'lix', 'lx', 'lxi', 'lxii',
    'lxiii', 'lxiv', 'lxv', 'lxvi', 'lxvii', 'lxviii', 'lxix', 'lxx',
    'lxxi', 'lxxii', 'lxxiii', 'lxxiv', 'lxxv', 'lxxvi', 'lxxvii',
    'lxxviii', 'lxxix', 'lxstopwordsxx', 'lxxxi', 'lxxxii', 'lxxxiii', 'lxxxiv',
    'lxxxv', 'lxxxvi', 'lxxxvii', 'lxxxviii', 'lxxxix', 'xc', 'xci',
    'xcii', 'xciii', 'xciv', 'xcv', 'xcvi', 'xcvii', 'xcviii', 'xcix', 'c'
])
try:
    stopwords = set(nltk_stopwords.words('english'))
except:
    stopwords = set()
    print('Warning: NLTK stopwords not used! Please check if the nltk stopwords corpus is avaialable in your system.')
stopwords.update(stop_words.ENGLISH_STOP_WORDS)
stopwords.update(roman_nums)

stopwords = list(stopwords)


# # Spelling correction module

# In[4]:


respell_error = []


class Respeller:

    en_dict = Dict('en_US') if ENCHANT_INSTALLED else pattern.en
    WORKERS = os.cpu_count() - 1

    def __init__(self, dictionary_file=None, spell_threshold=0.3, spell_cache=None):
        self.spell_cache = spell_cache if spell_cache is not None else {}  # pd.Series()
        self.dictionary_file = dictionary_file
        self.spell_threshold = spell_threshold
        self.stopwords = stopwords

        if (self.dictionary_file is not None) and os.path.isfile(self.dictionary_file):
            self.spell_cache = pd.read_csv(self.dictionary_file)

    def save_spell_cache(self):
        pd.Series(self.spell_cache).to_csv(self.dictionary_file)

    def morph_word(self, word):
        # word = word.replace(' ', '')  # Check if compound word suggestion matches the misspelled word
        # Perform this opperation to add more robustness to the matching
        m_word = word + ''.join(sorted(word))

        return m_word

    def infer_correct_word(self, word, sim_thresh=0.0, print_log=False, min_len=3, use_suggest_score=True):
        if word not in self.spell_cache:
            correct_word = None
            score = -1

            payload = dict(word=word, correct_word=correct_word, score=score)

            self.spell_cache[word] = payload

            if len(word) <= min_len:
                return self.spell_cache[word]

            candidates = self.en_dict.suggest(word)
            if not ENCHANT_INSTALLED:
                # Do this since pattern returns a tuple of (word, score)
                candidates = [w for w, sim in candidates if sim > 0.1]

            if use_suggest_score:
                suggest_score = 1 / rankdata(range(len(candidates)))**0.5
            else:
                suggest_score = np.ones(len(candidates))

            if candidates:
                try:
                    m_word = self.morph_word(word)
                    m_candidates = [self.morph_word(
                        c.lower()) for c in candidates]

                    tfidf = TfidfVectorizer(
                        analyzer='char', ngram_range=(2, 4))
                    candX = tfidf.fit_transform(m_candidates)
                    wordX = tfidf.transform([m_word])

                    r = 1.0 / rankdata([edit_distance(m_word, x)
                                        for x in m_candidates])

                    sim = cosine_similarity(candX, wordX)
                    sim_r = sim * r.reshape(-1, 1) * \
                        suggest_score.reshape(-1, 1)

                    sim_ind = sim_r.argmax()
                    score = sim_r[sim_ind]
                    if score > sim_thresh:
                        correct_word = candidates[sim_ind]
                except Exception as e:
                    # raise ValueError(word)
                    print(f"Error word: {word}")

            if print_log:
                print(sim_r)
                print(r)
                print(word)
                print(candidates)
                print(candidates[sim_ind])

            payload['correct_word'] = correct_word
            payload['score'] = float(score)

            self.spell_cache[word] = payload

        return self.spell_cache[word]

    def qualified_word(self, word):
        stopwords = set(self.stopwords)
        is_valid = (
            (word not in stopwords) and
            (not word[0].isupper()) and
            len(word) > 2
        )

        return is_valid

    def parallel_infer_correct_word(self, words, num_workers):
        respelled_set = {}

        respell_results = [self.infer_correct_word(ew) for ew in words]

        words = set([])

        for res in respell_results:
            word = res['word']
            correct_word = res['correct_word']
            score = res['score']

            if correct_word and score > self.spell_threshold:
                if correct_word.istitle():
                    # If the respelling results to a `Title` word
                    # it implies that the word is a proper noun, therefore, omit.
                    words.add(word)
                else:
                    # Split and filter since some words are compound terms.
                    respelled_set[word] = [
                        i for i in correct_word.split() if self.qualified_word(i)]
            else:
                words.add(word)

        return words, respelled_set


# # Optimized cleaner with internal parallelization support

# In[9]:


class Cleaner:

    from enchant.checker import SpellChecker

    input_folder = ''
    output_folder = ''
    custom_stopwords = []
    spellchecker = None
    respeller = None
    acronym_mapper = None
    lemma = None
    space_normalize_text_pattern = re.compile('[.\s]{2,}')
    noise_normalize_text_pattern = re.compile('[^a-z\'\.\?\!\s]+')
    short_valid_tokens_pattern = re.compile('[a-z]{3,}')
    long_invalid_tokens_pattern = re.compile('\w{25,}')

    spell_cache_manager = multiprocessing.Manager()
    spell_cache_dict = spell_cache_manager.dict()

    def __init__(
        self, use_spellchecker=False, use_respeller=False,
        use_lemmatizer=False, num_workers=None,
        ignore_length=50, use_spacy=True,
        replacements_plurals_to_singular_file=None,
        acronyms_file=None,
        min_en_lang_prob=0.98,
        supported_lang=('en',),
        logger=None,
        check_language=True
    ):
        self.data = []
        self.check_language = check_language
        self.use_spellchecker = use_spellchecker
        self.use_lemmatizer = use_lemmatizer
        self.use_respeller = use_respeller
        self.num_workers = (
            os.cpu_count() - 1) if num_workers is None else num_workers
        self.patterns = []
        self.lemma_cache = {}
        self.respelled_set = {}
        self.use_spacy_lemmatizer = use_spacy
        self.ignore_length = ignore_length
        self.ENCHANT_INSTALLED = ENCHANT_INSTALLED
        self.replacements_plurals_to_singular_file = replacements_plurals_to_singular_file
        self.acronyms_file = acronyms_file
        self.min_en_lang_prob = min_en_lang_prob
        self.supported_lang = supported_lang

        if logger:
            self.logger = logger.error
        else:
            self.logger = print

        self.plural_singular_map = {}

        if self.replacements_plurals_to_singular_file is not None:
            self.build_plurals_to_singular_map()

        if self.use_spellchecker:
            self.spellchecker = SpellChecker(
                "en_US") if ENCHANT_INSTALLED else pattern.en

        if self.use_lemmatizer:
            self.lmtzr_spacy = None  # spacy.load('en')
            self.lmtzr_wordnet = None if self.use_spacy_lemmatizer else WordNetLemmatizer()

        if self.use_respeller:
            self.respeller = Respeller(
                spell_threshold=0.7, spell_cache=self.spell_cache_dict)

        if self.acronyms_file is not None:
            self.acronym_mapper = AcronymMapper(
                whitelist_file=self.acronyms_file, sim_thresh=0.8)

        self.stopwords = stopwords

        # initialize clean_text
        self.clean_text('initialize cleaner')

    def build_plurals_to_singular_map(self):
        '''
        Assume that the whitelist is a two column excel file without a header: first col - plural, second col - singular.
        Don't catch exception such that any errors will be apparent.
        '''
        plural_singular_map = pd.read_csv(
            self.replacements_plurals_to_singular_file, header=None, index_col=0).dropna()[1]
        self.plural_singular_map = dict(plural_singular_map)

    def set_input_folder(self, input_folder):
        self.input_folder = input_folder

    def set_output_folder(self, output_folder):
        self.output_folder = output_folder
        if not os.path.isdir(self.output_folder):
            os.makedirs(self.output_folder)

    def set_custom_stopwords(self, stopwords):
        self.custom_stopwords = stopwords

    # remove noise words
    def remove_noise(self, text):
        text = text.lower()
        text = self.long_invalid_tokens_pattern.sub('', text)
        text = ' '.join(self.short_valid_tokens_pattern.findall(text))

        return text

    def get_lemma(self, word, word_pos):
        stopwords = set(self.stopwords)
        if word in stopwords:
            return None

        key = (word, word_pos)

        if key not in self.lemma_cache:
            lemma = self.lmtzr_wordnet.lemmatize(word, word_pos)
            self.lemma_cache[key] = lemma

        return self.lemma_cache[key]

    def lemmatize_text_wordnet(self, text):
        tokens = nltk.word_tokenize(text)

        txt_out = ''

        # Before lemmatizing, we tag words (part-of-speech tagging)
        tagged_tokens = pos_tag(tokens)

        # We now lemmatize based on a simplified list of POS tags
        for tagged_token in tagged_tokens:
            word = tagged_token[0]
            word_pos = tagged_token[1]

            # We recode NLTK tagging for consistency with wordnet
            if tagged_token[1].startswith('J'):
                word_pos = wordnet.ADJ
            elif tagged_token[1].startswith('V'):
                word_pos = wordnet.VERB
            elif tagged_token[1].startswith('N'):
                word_pos = wordnet.NOUN
            elif tagged_token[1].startswith('R'):
                word_pos = wordnet.ADV
            else:
                word_pos = wordnet.NOUN  # Assume noun if other

            # We now lemmatize, taking the POS tag into account
            lemma = self.get_lemma(word, word_pos)

            if lemma is not None:
                txt_out = txt_out + lemma + ' '

        return txt_out

    def lemmatize_text_spacy(self, text):
        stopwords = set(self.stopwords)
        try:
            lmtzr_spacy = spacy.load(
                'en', disable=['parser', 'ner', 'textcat'])
        except OSError:
            lmtzr_spacy = spacy.load(
                '/R/spacy_data/en_core_web_sm/en_core_web_sm-2.0.0', disable=['parser', 'ner', 'textcat'])

        doc = lmtzr_spacy(text.lower())
        # ' '.join(re.findall('[a-z0-9]+', text.lower())))

        txt_out = ''

        for token in doc:
            if token.lemma_ in stopwords:
                continue

            txt_out = txt_out + token.lemma_ + ' '

        txt_out = txt_out.replace('-PRON-', '')

        return txt_out.strip()

    def space_normalize_text(self, text):
        text = self.space_normalize_text_pattern.sub(' . ', text.lower())
        text = self.noise_normalize_text_pattern.sub(' ', text)
        return text

    def lemmatize_text(self, text):
        # Perform preliminary removal of noise
        text = self.space_normalize_text(text)

        txt_out = ''
        if self.use_spacy_lemmatizer:
            txt_out = self.lemmatize_text_spacy(text)
        else:
            txt_out = self.lemmatize_text_wordnet(text)

        return txt_out

    def get_misspelled_tokens(self, text):
        if self.spellchecker is None:
            raise ValueError('Spellchecker is not enabled')

        errors = set([])

        if ENCHANT_INSTALLED:
            # Input is a text
            self.spellchecker.set_text(text)

            for err in self.spellchecker:
                #print (err.word)
                if err.word not in self.respelled_set:
                    errors.add(err.word)
        else:
            # Input is a list of tokens
            text_tokens = set(text)
            for token in text_tokens:
                suggestions = self.spellchecker.suggest(token)

                # If suggestions are available, make sure that the first
                # suggestion is similar to the token to make sure
                # that the token being testing is a legit word.
                if suggestions and (suggestions[0][0] == token and suggestions[0][1] > 0.9):
                    continue
                else:
                    errors.add(token)
        return errors

    # Run spell checker on text to keep words found in dictionary only
    def spellcheck_text(self, text):
        text_tokens = word_tokenize(text)
        errors = self.get_misspelled_tokens(
            text if ENCHANT_INSTALLED else text_tokens)

        if errors and self.respeller:
            errors, respelled_set = self.respeller.parallel_infer_correct_word(
                errors, self.num_workers * 2)  # max((self.num_workers // 2), 1))
            # print(respelled_set)
            self.respelled_set.update(respelled_set)

        errors_set = set(errors)
        cleaned_text = []

        for x in text_tokens:
            if (x in errors_set):
                continue

            elif x in self.respelled_set:
                for x in self.respelled_set[x]:
                    x = self.plural_singular_map.get(x, x)
                    cleaned_text.append(x)

            elif (x in self.stopwords):
                continue

            else:
                x = self.plural_singular_map.get(x, x)
                cleaned_text.append(x)

        output = {}
        output['text'] = " ".join(cleaned_text)
        output['errors'] = errors

        return output

    def load_existing_and_extract_metadata(self, fileid, filepath, save_docs, process_output_dict=None):
        proc_fileid = fileid

        filename = filepath.split('/')[-1]
        fileid = filename.strip('.txt')

        with open(filepath) as fl:
            text = fl.read()

        lang_log = ('ERROR', 0)
        token_log = 0
        skipped_log = ''
        text_log = ''
        spell_errors = []
        exp = None
        write_status = True

        predict_lang = detect_langs(text)[0]
        lang_log = (predict_lang.lang, predict_lang.prob)
        # Log tokens count
        token_log = len(word_tokenize(text))
        text_log = text

        cleaning_output = dict(
            lang=lang_log,
            token=token_log,
            text=text_log,
            skipped=skipped_log,
            spell_errors=spell_errors,
            exception=exp,
            write_status=write_status,
        )

        # log statistics
        # lang info per document - uses the format - lang_log[fileid]={'score','lang'}
        lang_log = {}
        spell_errors = {}
        token_log = {}  # Tokens count per document
        text_errors = {}
        text_log = {}
        skipped_log = {}
        exception_log = {}
        write_status_log = {}

        lang_log[fileid] = cleaning_output['lang']
        token_log[fileid] = cleaning_output['token']
        skipped_log[fileid] = cleaning_output['skipped']
        text_log[fileid] = cleaning_output['text']
        spell_errors[fileid] = cleaning_output['spell_errors']
        exception_log[fileid] = cleaning_output['exception']
        write_status_log[fileid] = cleaning_output['write_status']

        # return logs
        output_log = {}
        output_log['lang'] = lang_log
        output_log['tokens'] = token_log
        output_log['text'] = text_log
        output_log['spell_errors'] = spell_errors
        output_log['skipped'] = skipped_log
        output_log['exception'] = exception_log
        output_log['write_status'] = write_status_log

        if process_output_dict is not None:
            process_output_dict[proc_fileid] = output_log
        else:
            return output_log

    def clean_text(self, text, filen=None):
        lang_log = ('ERROR', 0)
        token_log = 0
        skipped_log = ''
        text_log = ''
        spell_errors = []
        exp = None
        write_status = False

        if self.acronym_mapper is not None:
            text = self.acronym_mapper.expand_doc_acronyms(text)

        text = text.lower()
        len_text = len(text)

        if len_text > self.ignore_length:

            if self.use_lemmatizer:
                # Apply lemmatizer
                try:
                    text = self.lemmatize_text(text)
                except Exception as excp:
                    self.logger(f'Failed lemmatization for {filen}')
                    exp = excp.args[0]

            if exp is None:
                # Remove noise words e.g. punctuation, numbers, non-utf characters etc
                text = self.remove_noise(text)

                # Skip documents with no content
                if len(text) > 0:
                    # Detect majority language of the document
                    try:
                        predict_lang = detect_langs(text)[0]

                        lang_log = (predict_lang.lang, predict_lang.prob)

                        if self.check_language:
                            # Only process documents in English
                            if (any([predict_lang.lang == lg for lg in self.supported_lang])) and (predict_lang.prob >= self.min_en_lang_prob):
                                if self.use_spellchecker:
                                    # Run spell check and keep only the words found in dictionary
                                    spell_data = self.spellcheck_text(text)
                                    spell_errors = spell_data['errors']
                                    text = spell_data['text']

                                # Log tokens count
                                token_log = len(word_tokenize(text))
                                write_status = True
                            else:
                                # not in english
                                skipped_log = f'Not in english | {predict_lang}'
                        else:
                            if self.use_spellchecker:
                                # Run spell check and keep only the words found in dictionary
                                spell_data = self.spellcheck_text(text)
                                spell_errors = spell_data['errors']
                                text = spell_data['text']

                            # Log tokens count
                            token_log = len(word_tokenize(text))
                            write_status = True

                    except Exception as excp:
                        skipped_log = f"Error detecting language for = {filen}. {excp.args[0]}"
                        self.logger(skipped_log)
                        exp = excp.args[0]
                else:
                    skipped_log = f"Empty doc post lemmatizer = {filen}"
                    self.logger(skipped_log)
                    # Log tokens count
        else:
            skipped_log = f"Doclen {len_text} < {self.ignore_length} = {filen}"
            self.logger(skipped_log)
            # Log tokens count
            token_log = 0

        text_log = text

        payload = dict(
            lang=lang_log,
            token=token_log,
            text=text_log,
            skipped=skipped_log,
            spell_errors=spell_errors,
            exception=exp,
            write_status=write_status,
        )

        payload = {k: v if not isinstance(v, set) else list(
            v) for k, v in payload.items()}
        return payload


# In[6]:


class CorpusCleaner(Cleaner):

    # Clean documents using spell checker
    def batch_clean_docs(self, doclist, batch_size=None, save_docs=False, collect_text_log=False, collect_spell_errors=False, skip_existing=True, default_docs_per_worker=20):
        if batch_size is None:
            # Use a multiplier for efficient usage of workers
            batch_size = default_docs_per_worker * self.num_workers

        file_counter_x = 0
        input_folder = self.input_folder
        output_folder = self.output_folder

        # log statistics
        # Lang info per document - uses the format - lang_log[fileid]=('lang', 'score')
        lang_log = {}
        text_log = {}  # Errors count per document
        token_log = {}  # Tokens count per document
        skipped_log = {}  # Documents not processed
        spell_errors = {}
        exception_log = {}
        write_status_log = {}

        log_interval = batch_size

        with Parallel(n_jobs=self.num_workers, backend='multiprocessing') as pool:
            # Cleaning all text files found in input in folder
            batch = []
            for ix, fileid in enumerate(doclist):
                if ix % log_interval == 0:
                    self.logger(f'Docset {ix}')

                file_counter_x += 1
                if fileid.endswith('.txt'):    # text files only

                    filen = os.path.join(input_folder, fileid)     # input file
                    newfile = os.path.join(
                        output_folder, fileid)   # output file

                    if not os.path.isfile(filen):
                        self.logger(f"No input file: {fileid}")
                        continue

                    # Skip if output file already exists
                    if os.path.isfile(newfile) and skip_existing:
                        # self.logger(f"Output file exists: {fileid}. Skipping...")
                        continue

                    if len(batch) != batch_size:
                        batch.append(filen)

                    else:
                        with Timer() as timer:
                            doc_outputs = pool((delayed(self.clean_doc)(
                                fln, save_doc=save_docs) for fln in batch))
                            # doc_outputs = Parallel(n_jobs=self.num_workers, backend='multiprocessing')(delayed(self.clean_doc)(fln, save_doc=save_docs) for fln in batch)
                            # doc_outputs = pool.map(self.clean_doc, [(fln, save_docs) for fln in batch], chunksize=batch_size)

                            for doc_output in doc_outputs:

                                lang_log.update(doc_output['lang'])
                                token_log.update(doc_output['tokens'])
                                skipped_log.update(doc_output['skipped'])
                                exception_log.update(doc_output['exception'])
                                write_status_log.update(
                                    doc_output['write_status'])

                                if collect_text_log:
                                    # Don't do this if you're processing a lot of docs
                                    text_log.update(doc_output['text'])
                                if collect_spell_errors:
                                    spell_errors.update(
                                        doc_output['spell_errors'])

                            batch = []

                        self.logger(
                            f'Set {ix}: {log_interval} items for {timer.elapsed:.2f} seconds.')

            if batch:
                doc_outputs = pool((delayed(self.clean_doc)(
                    fln, save_doc=save_docs) for fln in batch))
                # doc_outputs = Parallel(n_jobs=self.num_workers, backend='multiprocessing')(delayed(self.clean_doc)(fln, save_doc=save_docs) for fln in batch)
                # doc_outputs = pool.map(self.clean_doc, [(fln, save_docs) for fln in batch], chunksize=batch_size)

                for doc_output in doc_outputs:

                    lang_log.update(doc_output['lang'])
                    token_log.update(doc_output['tokens'])
                    skipped_log.update(doc_output['skipped'])
                    exception_log.update(doc_output['exception'])
                    write_status_log.update(doc_output['write_status'])

                    if collect_text_log:
                        # Don't do this if you're processing a lot of docs
                        text_log.update(doc_output['text'])
                    if collect_spell_errors:
                        spell_errors.update(doc_output['spell_errors'])

        output_log = {}
        output_log['lang'] = lang_log
        output_log['tokens'] = token_log
        output_log['text'] = text_log
        output_log['spell_errors'] = spell_errors
        output_log['skipped'] = skipped_log
        output_log['exception'] = exception_log
        output_log['write_status'] = write_status_log

        return output_log

    # Clean a single document using spell checker
    def clean_doc(self, filepath, save_doc=False):  # args):
        # filepath, *save_doc = args

        if save_doc is None:
            save_doc = False

        # log statistics
        # lang info per document - uses the format - lang_log[fileid]={'score','lang'}
        lang_log = {}
        spell_errors = {}
        token_log = {}  # Tokens count per document
        text_errors = {}
        text_log = {}
        skipped_log = {}
        exception_log = {}
        write_status_log = {}

        filename = filepath.split('/')[-1]

        fileid = filename.strip('.txt')

        with open(filepath, 'rb') as fl:
            # Use context so that the file will be closed automatically upon exit from the context.
            text = fl.read()
            text = text.decode('utf-8', errors='ignore')

        cleaning_output = self.clean_text(text, filen=fileid)
        text = cleaning_output['text']

        lang_log[fileid] = cleaning_output['lang']
        token_log[fileid] = cleaning_output['token']
        skipped_log[fileid] = cleaning_output['skipped']
        text_log[fileid] = text
        spell_errors[fileid] = cleaning_output['spell_errors']
        exception_log[fileid] = cleaning_output['exception']
        write_status_log[fileid] = cleaning_output['write_status']

        if save_doc and cleaning_output['write_status']:
            with open(os.path.join(self.output_folder, filename), 'w') as fl:
                fl.write(text)

        # return logs
        output_log = {}
        output_log['lang'] = lang_log
        output_log['tokens'] = token_log
        output_log['text'] = text_log
        output_log['spell_errors'] = spell_errors
        output_log['skipped'] = skipped_log
        output_log['exception'] = exception_log
        output_log['write_status'] = write_status_log

        return output_log


# In[7]:


class ParallelCorpusCleaner(Cleaner):

    # Clean documents using spell checker
    def batch_clean_docs(self, doclist, batch_size=None, save_docs=False, collect_text_log=False, collect_spell_errors=False, skip_existing=True):
        if batch_size is None:
            # Use a multiplier for efficient usage of workers
            batch_size = 4 * self.num_workers

        file_counter_x = 0
        input_folder = self.input_folder
        output_folder = self.output_folder

        # log statistics
        # Lang info per document - uses the format - lang_log[fileid]=('lang', 'score')
        lang_log = {}
        text_log = {}  # Errors count per document
        token_log = {}  # Tokens count per document
        skipped_log = {}  # Documents not processed
        spell_errors = {}
        exception_log = {}
        write_status_log = {}

        log_interval = batch_size

        process_output_manager = multiprocessing.Manager()
        process_output_dict = process_output_manager.dict()

        batch = {}
        ix = 0
        while True:
            try:
                if len(batch) < batch_size:
                    fileid = doclist.pop(0)
                    # print(f'Processing {ix}: {fileid}')
                    ix += 1

                    if ix % log_interval == 0:
                        self.logger(f'Docset {ix}')

                    if fileid.endswith('.txt'):    # text files only
                        filen = os.path.join(
                            input_folder, fileid)     # input file
                        newfile = os.path.join(
                            output_folder, fileid)   # output file

                        if not os.path.isfile(filen):
                            self.logger(f"No input file: {fileid}")
                            continue

                        # Skip if output file already exists
                        if os.path.isfile(newfile) and skip_existing:
                            p = multiprocessing.Process(target=self.load_existing_and_extract_metadata, args=(
                                fileid, newfile, save_docs, process_output_dict))  # , kwargs=kwargs)
                            batch[fileid] = p
                            p.start()
                            # self.logger(f"Output file exists: {fileid}. Skipping...")
                            continue

                        # kwargs = {'process_output_dict': process_output_dict, 'save_doc': save_docs}
                        p = multiprocessing.Process(target=self.clean_doc, args=(
                            fileid, filen, save_docs, process_output_dict))  # , kwargs=kwargs)
                        batch[fileid] = p
                        p.start()
                else:
                    completed_data = set(process_output_dict.keys())

                    for fld in completed_data:
                        # print(f'Completed {fld}')
                        if fld not in batch:
                            continue
                        pk = batch.pop(fld)
                        pk.join()

                        # This shouldn't be necessary but still doing this just to be safe... :)
                        if pk.is_alive():
                            pk.terminate()
                            pk.join()

                        fileid = doclist.pop(0)
                        ix += 1

                        # print(f'Starting {fileid}')

                        if ix % log_interval == 0:
                            self.logger(f'Docset {ix}')

                        if fileid.endswith('.txt'):    # text files only
                            filen = os.path.join(
                                input_folder, fileid)     # input file
                            newfile = os.path.join(
                                output_folder, fileid)   # output file

                            if not os.path.isfile(filen):
                                self.logger(f"No input file: {fileid}")
                                continue

                            # Skip if output file already exists
                            if os.path.isfile(newfile) and skip_existing:
                                p = multiprocessing.Process(target=self.load_existing_and_extract_metadata, args=(
                                    fileid, newfile, save_docs, process_output_dict))  # , kwargs=kwargs)
                                batch[fileid] = p
                                p.start()
                                # self.logger(f"Output file exists: {fileid}. Skipping...")
                                continue

                            # kwargs = {'process_output_dict': process_output_dict, 'save_doc': save_docs}
                            p = multiprocessing.Process(target=self.clean_doc, args=(
                                fileid, filen, save_docs, process_output_dict))  # , kwargs=kwargs)
                            batch[fileid] = p
                            p.start()

            except Exception as e:
                print(f'Exception received: {e.args[0]}')
                bfileids = set(batch.keys())
                for fileid in bfileids:
                    p = batch.pop(fileid)
                    p.join()

                    if p.is_alive():
                        p.terminate()
                        p.join()
                break

        # Cleanup just in case...
        bfileids = set(batch.keys())
        for fileid in bfileids:
            p = batch.pop(fileid)
            p.join()

            if p.is_alive():
                p.terminate()
                p.join()

        for fileid in process_output_dict.keys():
            doc_output = process_output_dict[fileid]

            lang_log.update(doc_output['lang'])
            token_log.update(doc_output['tokens'])
            skipped_log.update(doc_output['skipped'])
            exception_log.update(doc_output['exception'])
            write_status_log.update(doc_output['write_status'])

            if collect_text_log:
                # Don't do this if you're processing a lot of docs
                text_log.update(doc_output['text'])
            if collect_spell_errors:
                spell_errors.update(doc_output['spell_errors'])

        output_log = {}
        output_log['lang'] = lang_log
        output_log['tokens'] = token_log
        output_log['text'] = text_log
        output_log['spell_errors'] = spell_errors
        output_log['skipped'] = skipped_log
        output_log['exception'] = exception_log
        output_log['write_status'] = write_status_log

        return output_log

    # Clean a single document using spell checker
    # args):
    def clean_doc(self, fileid, filepath, save_doc=False, process_output_dict=None):
        proc_fileid = fileid
        # filepath, *save_doc = args

        if save_doc is None:
            save_doc = False

        # log statistics
        # lang info per document - uses the format - lang_log[fileid]={'score','lang'}
        lang_log = {}
        spell_errors = {}
        token_log = {}  # Tokens count per document
        text_errors = {}
        text_log = {}
        skipped_log = {}
        exception_log = {}
        write_status_log = {}

        filename = filepath.split('/')[-1]

        fileid = filename.strip('.txt')

        with open(filepath, 'rb') as fl:
            # Use context so that the file will be closed automatically upon exit from the context.
            text = fl.read()
            text = text.decode('utf-8', errors='ignore')
            text = text.lower()

        cleaning_output = self.clean_text(text, filen=fileid)
        text = cleaning_output['text']

        lang_log[fileid] = cleaning_output['lang']
        token_log[fileid] = cleaning_output['token']
        skipped_log[fileid] = cleaning_output['skipped']
        text_log[fileid] = text
        spell_errors[fileid] = cleaning_output['spell_errors']
        exception_log[fileid] = cleaning_output['exception']
        write_status_log[fileid] = cleaning_output['write_status']

        if save_doc and cleaning_output['write_status']:
            with open(os.path.join(self.output_folder, filename), 'w') as fl:
                fl.write(text)

        # return logs
        output_log = {}
        output_log['lang'] = lang_log
        output_log['tokens'] = token_log
        output_log['text'] = text_log
        output_log['spell_errors'] = spell_errors
        output_log['skipped'] = skipped_log
        output_log['exception'] = exception_log
        output_log['write_status'] = write_status_log

        if process_output_dict is not None:
            process_output_dict[proc_fileid] = output_log
        else:
            return output_log


# In[8]:


# payload = dict(
#     lang=lang_log,
#     token=token_log,
#     text=text_log,
#     skipped=skipped_log,
#     spell_errors=spell_errors,
#     exception=exp,
#     write_status=write_status,
# )

# payload = {k: v if not isinstance(v, set) else list(v) for k, v in payload.items()}

# Input document text and process documents with at least `ignore_length` characters.

# Step 1: Detect countries from the document if a country map file is provided.
# Step 2: Apply lemmatization if specified (lemmatizer options: spacy or nltk).
# In[ ]:

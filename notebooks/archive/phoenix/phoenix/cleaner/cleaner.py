import os
import re
import numpy as np
import pandas as pd
import nltk

nltk.data.path.append("/R/nltk_data")

from nltk.corpus import words
from nltk.corpus import PlaintextCorpusReader, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag

from langdetect import detect, detect_langs

from joblib import Parallel, delayed
import multiprocessing as mp
import multiprocessing

import spacy
import multiprocessing

from phoenix.acronyms.acronyms import AcronymMapper

from phoenix.cleaner.stopwords import stopwords
from phoenix.cleaner.respelling import OptimizedSpellChecker, Respeller


# Prevent this error in spacy
# ---------------------------------------------------
# Text of length 1213412 exceeds maximum of 1000000.
# The v2.x parser and NER models require roughly 1GB of temporary memory per 100,000 characters in the input.
# This means long texts may cause memory allocation errors.
# If you're not using the parser or NER, it's probably safe to increase the `nlp.max_length` limit.
# The limit is in number of characters, so you can check whether your inputs are too long by checking `len(text)`."
# ---------------------------------------------------
SPACY_MAX_LENGTH = 10 * 1000000

try:
    _lmtzr_spacy = spacy.load('en', disable=['parser', 'ner', 'textcat'], max_length=SPACY_MAX_LENGTH)
except OSError:
    # _lmtzr_spacy = spacy.load('/R/spacy_data/en_core_web_sm/en_core_web_sm-2.0.0', disable=['parser', 'ner', 'textcat'], max_length=SPACY_MAX_LENGTH)
    _lmtzr_spacy = spacy.load('en_core_web_sm', disable=['parser', 'ner', 'textcat'], max_length=SPACY_MAX_LENGTH)

class Cleaner:
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
        check_language=True,
        spell_threshold=0.7,
    ):
        self.data=[]
        self.check_language = check_language
        self.use_spellchecker = use_spellchecker
        self.use_lemmatizer = use_lemmatizer
        self.use_respeller = use_respeller
        self.num_workers = (os.cpu_count() - 1) if num_workers is None else num_workers
        self.patterns = []
        self.lemma_cache = {}
        self.respelled_set = {}
        self.use_spacy_lemmatizer = use_spacy
        self.ignore_length = ignore_length
        self.replacements_plurals_to_singular_file = replacements_plurals_to_singular_file
        self.acronyms_file = acronyms_file
        self.min_en_lang_prob = min_en_lang_prob
        self.supported_lang = supported_lang
        self.spell_threshold = spell_threshold

        if logger:
            self.logger = logger.error
        else:
            self.logger = print

        self.plural_singular_map = {}

        if self.replacements_plurals_to_singular_file is not None:
            self.build_plurals_to_singular_map()

        if self.use_spellchecker:
            self.spellchecker = OptimizedSpellChecker("en_US")

        if self.use_lemmatizer:
            self.lmtzr_spacy = None  # spacy.load('en')
            self.lmtzr_wordnet = None if self.use_spacy_lemmatizer else WordNetLemmatizer()

        if self.use_respeller:
            self.respeller = Respeller(spell_threshold=self.spell_threshold, spell_cache=self.spell_cache_dict)

        if self.acronyms_file is not None:
            self.acronym_mapper = AcronymMapper(whitelist_file=self.acronyms_file, sim_thresh=0.8)

        self.stopwords = stopwords

        # initialize clean_text
        self.clean_text('initialize cleaner')

    def build_plurals_to_singular_map(self):
        '''
        Assume that the whitelist is a two column excel file without a header: first col - plural, second col - singular.
        Don't catch exception such that any errors will be apparent.
        '''
        plural_singular_map = pd.read_csv(self.replacements_plurals_to_singular_file, header=None, index_col=0).dropna()[1]
        self.plural_singular_map = dict(plural_singular_map)

    def set_input_folder(self,input_folder):
        self.input_folder = input_folder

    def set_output_folder(self,output_folder):
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
                word_pos = wordnet.NOUN # Assume noun if other

            # We now lemmatize, taking the POS tag into account
            lemma = self.get_lemma(word, word_pos)

            if lemma is not None:
                txt_out = txt_out + lemma + ' '

        return txt_out

    def lemmatize_text_spacy(self, text):
        stopwords = set(self.stopwords)
#         try:
#             lmtzr_spacy = spacy.load('en', disable=['parser', 'ner', 'textcat'])
#         except OSError:
#             lmtzr_spacy = spacy.load('/R/spacy_data/en_core_web_sm/en_core_web_sm-2.0.0', disable=['parser', 'ner', 'textcat'])

        doc = _lmtzr_spacy(text.lower())
            # ' '.join(re.findall('[a-z0-9]+', text.lower())))

        txt_out = [token.lemma_ for token in doc if token.lemma_ not in stopwords]
        txt_out = ' '.join(txt_out)
        txt_out = txt_out.replace('-PRON-', '')

        return txt_out

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

        # Input is a list of tokens
        text_tokens = set(text)
        self.spellchecker.set_tokens(text)

        for err in self.spellchecker:
            # print (err.word)
            if err.word not in self.respelled_set:
                errors.add(err.word)

        return errors

    # Run spell checker on text to keep words found in dictionary only
    def spellcheck_text(self, text):
        text_tokens=word_tokenize(text)
        errors = self.get_misspelled_tokens(text_tokens)

        if errors and self.respeller:
            errors, respelled_set = self.respeller.parallel_infer_correct_word(errors, self.num_workers * 2)  # max((self.num_workers // 2), 1))
            # print(respelled_set)
            self.respelled_set.update(respelled_set)

        errors_set=set(errors)
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

        output={}
        output['text']=" ".join(cleaned_text)
        output['errors']=errors

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
        lang_log = {}  # lang info per document - uses the format - lang_log[fileid]={'score','lang'}
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
                            if (any([predict_lang.lang == lg for lg in self.supported_lang])) and (predict_lang.prob >= self.min_en_lang_prob):   # Only process documents in English
                                if self.use_spellchecker:
                                    # Run spell check and keep only the words found in dictionary
                                    spell_data = self.spellcheck_text(text)
                                    spell_errors = spell_data['errors']
                                    text = spell_data['text']

                                # Log tokens count
                                token_log = len(word_tokenize(text))
                                write_status = True
                            else:
                                #not in english
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

        payload = {k: v if not isinstance(v, set) else list(v) for k, v in payload.items()}
        return payload

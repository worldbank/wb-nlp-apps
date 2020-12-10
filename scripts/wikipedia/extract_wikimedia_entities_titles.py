#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script processes the text data to generate candidate phrases based on part-of-speech patterns.
'''
import logging
from pathlib import Path
import gzip
import json
import re

import click

from gensim import utils
from joblib import Parallel, delayed
import joblib
import wb_nlp
from wb_nlp.utils.scripts import configure_logger, create_dask_cluster

MAX_LENGTH = 1000000


'''
Notes:
1. Download entities data from https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2 and save in /data/external/wikipedia/latest-all.json.bz2
2. Run `python -u ./scripts/wikipedia/extract_wikimedia_entities_titles.py --input-file ./data/external/wikipedia/latest-all.json.bz2 --output-file ./data/external/wikipedia/latest-all.wikimedia-titles.json  |& tee ./logs/extract_wikimedia_entities_titles.py.log`

Algorithm:
1. For each entity, check if not in excluded items or doesn't contain properties in the excluded properties list.
2. If OK in step 1, check the numbeer of wikipedia pages that are available about the entity. General concepts should, ideally, have wikipedia articles in the major languages.
3. Titles should not have accented characters.
4.

Excluded lists:
1. Names of people
2. Names of places
3. Everything that is tied with a country, e.g., companies, work of art, etc.

Use all words in the title with at least 3 characters.

JSON data schema description: https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON
'''

P_INTRO_NOISE_PATTERN = re.compile(r'[^a-zA-Z0-9\-., ]')
P_BDAY = re.compile(
    '(?:([A-Z][a-z]+ [0-9]{1,2}, [0-9]{1,4})|([0-9]{1,2} [A-Z][a-z]+ [0-9]{1,4}))')
P_ASCII = re.compile('^[ -~]+$')
GENSIM_BOLD_PATTERN = "'''"

INSTANCE_OF_PROPERTY = 'P31'
EXCLUDE_LIST_PROPERTIES = set([
    # https://www.wikidata.org/wiki/Property:P495
    'P495',     # - country of origin
    'P21',      # - sex or gender
    'P27',      # - country of citizenship
    'P17',      # - country
    'P276',     # - location
    'P50',      # - author
    'P170',     # - creator
    'P136',     # - genre
    'P175',     # - performer
])

EXCLUDE_LIST_ITEMS = set([
    # https://www.wikidata.org/wiki/Q23810017
    'Q5',            # - human
    'Q23810017',     # - decree
    'Q35749',        # - parliament
    'Q1197685',      # - public holiday
    'Q10876391',     # - Wikipedia language edition
    'Q7366',         # - song
    'Q4167410',      # - Wikipedia disambiguation page
    'Q4167836',      # - Wikimedia category
    'Q14795564',     # - point in time with respect to recurrent timeframe
    'Q13406463',     # - Wikimedia list article
    'Q80096233',     # - information list
])

IGNORED_NAMESPACES = [
    'Wikipedia', 'Category', 'File', 'Portal', 'Template',
    'MediaWiki', 'User', 'Help', 'Book', 'Draft', 'WikiProject',
    'Special', 'Talk'
]

IGNORED_GENERIC_STARTS = [
    'history of',
    'list of',
]

# https://www.babbel.com/en/magazine/the-10-most-spoken-languages-in-the-world
MAJOR_LANG_WIKIS = set([
    'enwiki',  # English
    'zhwiki',  # Chinese
    'hiwiki',  # Hindi
    'eswiki',  # Spanish
    'frwiki',  # French
    'arwiki',  # Arabic
    'bnwiki',  # Bangla/Bengali
    'ruwiki',  # Russian
    'ptwiki',  # Portuguese
    'idwiki',  # Indonesian
])


def get_mainsnak_value(ms):
    '''
    Crawl the mainsnak entry to get the snak value id.
    '''
    value = ''
    if ms is not None:
        if ms.get('mainsnak') is not None:
            if ms.get('mainsnak').get('datavalue') is not None:
                if ms.get('mainsnak').get('datavalue').get('value') is not None:
                    value = ms.get('mainsnak').get(
                        'datavalue').get('value').get('id')
    return value


def process_data_entry(data_entry):
    '''
    This function extracts the title and first line of the intro of the wiki article.
    There's an assumption that the first line of a wiki intro succinctly describes the article itself.
    This succinct description, together with the title, may be used as reference to filter useful phrases.

    The return format is a tuple. The first value is the title and the second is the intro. This is designed
    so that it's easy to generate a dictionary from the list of such tuples, i.e., result of joblib parallel processing.
    '''
    try:
        entry = json.loads(data_entry.rstrip(b',\n'))
    except:
        return dict(
            id=data_entry,
            label='',
            valid=False)

    entry_label = entry['labels'].get('en', {}).get('value', '')
    is_invalid_instance = False
    if entry['claims'].get(INSTANCE_OF_PROPERTY):
        is_invalid_instance = len(EXCLUDE_LIST_ITEMS.intersection(
            [get_mainsnak_value(ms) for ms in entry['claims'].get(
                INSTANCE_OF_PROPERTY)]
        )) > 0

    if (
        # Make sure the entry has an English label
        entry_label == '' or

        # Make sure the entry is an item
        entry['type'] != 'item' or

        # Include only entries that are not instances of the excluded items list
        is_invalid_instance or

        # Include only entities that don't have properties in the excluded list
        set(entry['claims']).intersection(EXCLUDE_LIST_PROPERTIES) or

        # Make sure there's an English wiki site for the entry
        entry['sitelinks'].get('enwiki', None) is None or

        any([entry_label.startswith(f'{ignored_ns}:') for ignored_ns in IGNORED_NAMESPACES]) or
        any([entry_label.lower().startswith(ignored_start) for ignored_start in IGNORED_GENERIC_STARTS]) or

        # The entry must have wiki site available in at least 5 of the 10 top spoken languages.
        len(MAJOR_LANG_WIKIS.intersection(entry['sitelinks'])) < 5
    ):
        return dict(
            id=entry['id'],
            label=entry_label,
            valid=False)

    payload = dict(
        id=entry['id'],
        label=entry_label,
        valid=True)

    if (
            entry_label.isdigit() or
            entry_label.isupper() or
            entry_label[0].isdigit() or
            len(entry_label) <= 2 or
            P_ASCII.search(entry_label) is None
    ):
        payload['valid'] = None

    return payload


_logger = logging.getLogger(__file__)


@ click.command()
@ click.option('--input-file', 'input_file', required=True,
               type=click.Path(exists=True), help='path to wiki articles generated by gensim.scripts.segment_wiki')
@ click.option('--output-file', 'output_file', required=True,
               type=click.Path(exists=False), help='path to output json file of article titles and intros')
@ click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@ click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@ click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@ click.option('--n-workers', 'n_workers', required=False, default=None)
@ click.option('--batch-size', 'batch_size', required=False, default=None)
@ click.version_option(wb_nlp.__version__)
def main(input_file: Path, output_file: Path, log_level: int, n_workers: int = None, batch_size: int = None):
    '''
    Entry point for wikimedia data filtering and title extraction script.
    '''
    configure_logger(log_level)

    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    input_file = Path(input_file)
    output_file = Path(output_file)

    logging.info('Checking files...')
    if not input_file.exists():
        raise ValueError("Input file doesn't exist!")

    if not output_file.resolve().parent.exists():
        output_file.resolve().parent.mkdir(parents=True)

    client = create_dask_cluster(_logger, n_workers=n_workers)
    _logger.info(client)

    _logger.info('Starting joblib tasks...')

    with utils.open(input_file, 'rb') as wiki_gz:
        with joblib.parallel_backend('dask'):
            batch_size = 'auto' if batch_size is None else int(batch_size)

            res = Parallel(verbose=10, batch_size=batch_size)(
                delayed(process_data_entry)(line) for line in wiki_gz)

    if output_file.name.endswith('.gz'):
        with gzip.open(output_file, mode='wt', encoding='utf-8') as gz_file:
            json.dump(list(filter(lambda x: x['valid'], res)), gz_file)
    else:
        with open(output_file, 'w') as out:
            json.dump(list(filter(lambda x: x['valid'], res)), out)

    _logger.info('Processed all: %s', all(res))

# Parameters:
# - Location of input data
# - Directory of * .txt files
# - MongoDB database


if __name__ == '__main__':
    # python -u ./scripts/wikipedia/extract_wikimedia_entities_titles.py --input-file ./data/external/wikipedia/sample-latest-all.json.bz2 --output-file ./data/external/wikipedia/sample-latest-all.wikimedia-titles.json -vv |& tee ./logs/extract_wikimedia_entities_titles.py.log
    main()


# '''
# https://www.wikidata.org/w/index.php?title=Special:WhatLinksHere/Q5&limit=500
# https://www.wikidata.org/w/index.php?title=Special:WhatLinksHere/Q5&namespace=0&limit=500&from=7130&back=4035
# https://meta.wikimedia.org/wiki/Data_dumps
# https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON


# '''
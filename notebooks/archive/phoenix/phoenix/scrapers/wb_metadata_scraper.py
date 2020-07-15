import requests
import json
import os
import time
import glob
import pandas as pd
import re
from joblib import Parallel, delayed
from phoenix.path_manager import get_corpus_path
from phoenix.dataset.document import DocumentDB

from phoenix.scrapers.utils import (
    download_with_retry,
    normalize_str_col,
    collapse_array,
    collapse_nested_dict,
    make_unique_entry,
    normalize_geo_regions
)


fl_params = [
    'guid', 'abstracts', 'admreg', 'alt_title', 'authr', 'available_in',
    'bdmdt', 'chronical_docm_id', 'closedt', 'colti', 'count', 'credit_no',
    'disclosure_date', 'disclosure_type', 'disclosure_type_date', 'disclstat',
    'display_title', 'docdt', 'docm_id', 'docna', 'docty', 'dois', 'entityid',
    'envcat', 'geo_reg', 'geo_reg_and_mdk', 'historic_topic', 'id',
    'isbn', 'issn', 'keywd', 'lang', 'listing_relative_url', 'lndinstr', 'loan_no',
    'majdocty', 'majtheme', 'ml_abstract', 'ml_display_title', 'new_url', 'owner',
    'pdfurl', 'prdln', 'projn', 'publishtoextweb_dt', 'repnb', 'repnme', 'seccl',
    'sectr', 'src_cit', 'subsc', 'subtopic', 'teratopic', 'theme', 'topic', 'topicv3',
    'totvolnb', 'trustfund', 'txturl', 'unregnbr', 'url_friendly_title', 'versiontyp',
    'versiontyp_key', 'virt_coll', 'vol_title', 'volnb', 'projectid',
]


SCRAPER_DIR = get_corpus_path('WB')
API_JSON_DIR = os.path.join(SCRAPER_DIR, 'tmp_api_json')


def request_worldbank_api(fl_params=None, offset=0, limit=1, max_retries=10):
    '''
    fl_params: list of values to return per row
    offset: parameter corresponding to the start page
    limit: maximum number of rows returned by the api call
    '''

    if fl_params is None:
        fl_params = ['guid']

    api_url = 'http://search.worldbank.org/api/v2/wds'
    api_params = dict(
        format='json',
        fl=','.join(fl_params),
        lang_exact='English',
        disclstat='Disclosed',
        srt='docdt',
        order='desc',  # Use asc such that pages already downloaded can still be used
        os=offset,
        rows=limit,
        # frmdisclosuredate='',  # '2018-09-12'
        # todisclosuredate='',  # '2018-09-13'
    )

    response = download_with_retry(url=api_url, params=api_params)

    if (response is None) or (response.status_code != 200):
        return {}

    json_content = response.json()

    return json_content


def get_total_documents():
    # This method solves the problem of determination of
    # the total pages in the database automatically.

    poll_request = request_worldbank_api()
    total_documents = poll_request['total']

    return int(total_documents)


def scrape_page(fl_params, page, limit=500, verbose=True, store_to_file=True):
    offset = page * limit
    page_content = request_worldbank_api(fl_params=fl_params, offset=offset, limit=limit)
    page_content = page_content['documents']
    func_params = {'page': page}

    # Remove extraneous key
    page_content.pop('facets')

    if store_to_file:
        if not os.path.isdir(API_JSON_DIR):
            os.makedirs(API_JSON_DIR)

        page_file = os.path.join(API_JSON_DIR, 'data-{page}.json'.format(**func_params))

        with open(page_file, 'w') as fl:
            json.dump(page_content, fl)

        if verbose:
            print('Completed scraping of page {page}.'.format(**func_params))

        time.sleep(1)
    else:
        return page_content


def scrape_worldbank_operational_docs_api(fl_params, limit=500, max_pages=5, n_jobs=1, verbose=False, to_celery=True):
    '''
    Note:
        Parallelization of API access is discouraged for large limit size.
        It could result to throttling or failed return values.
    '''
    func_params = {}
    total_documents = get_total_documents()

    total_pages = (total_documents // limit) + 1
    func_params['total_pages'] = total_pages

    scrape_params = []

    for page in range(total_pages):
        func_params['page'] = page + 1

        if (max_pages is not None) and (page > max_pages):
            print('Terminating scraping for remaining pages...')
            break
        if verbose:
            print('Scraping page {page} / {total_pages}'.format(**func_params))

        scrape_params.append(dict(fl_params=fl_params, page=page, limit=limit, verbose=verbose))

    if to_celery:
        from phoenix.tasks.wb_metadata_scraper_tasks import scrape_and_store_page
        async_objs = {sp['page']: scrape_and_store_page.delay(sp) for sp in scrape_params}

        return async_objs
    else:
        Parallel(n_jobs=n_jobs)(delayed(scrape_page)(**sp) for sp in scrape_params)


# ! Processing and normalization of scraped document metadata

def normalize_page_content(page_content, use_short_columns=True):
    # if use_short_columns:
    #     columns = ['guid', 'docyear', 'majdoctype', 'doctype', 'authors', 'colti', 'display_title', 'docdt', 'docm_id', 'historic_topic', 'pdfurl', 'seccl', 'txturl', 'language', 'admreg', 'country', 'txtfilename']
    # else:
    #     columns = ['authors', 'abstracts', 'admreg', 'alt_title', 'available_in', 'bdmdt', 'chronical_docm_id', 'closedt', 'colti', 'count', 'credit_no', 'disclosure_date', 'disclosure_type', 'disclosure_type_date', 'disclstat', 'display_title', 'docdt', 'doc_year', 'docm_id', 'docna', 'docty', 'dois', 'entityids', 'envcat', 'geo_regions', 'geo_region_mdks', 'historic_topic', 'id', 'isbn', 'issn', 'keywd', 'lang', 'listing_relative_url', 'lndinstr', 'loan_no', 'majdocty', 'majtheme', 'ml_abstract', 'ml_display_title', 'new_url', 'owner', 'pdfurl', 'prdln', 'projn', 'publishtoextweb_dt', 'repnb', 'repnme', 'seccl', 'sectr', 'src_cit', 'subsc', 'subtopic', 'teratopic', 'theme', 'topic', 'topicv3', 'totvolnb', 'trustfund', 'txturl', 'unregnbr', 'url_friendly_title', 'versiontyp', 'versiontyp_key', 'virt_coll', 'vol_title', 'volnb']

    normalized_data = pd.DataFrame(page_content).T
    normalized_data.index.name = 'uid'
    normalized_data.index = normalized_data.index.str.strip('D') # The API updated the format of `uid` by adding a `D` prefix to the original format.
    normalized_data.index = normalized_data.index.astype(int)

    rename_cols = {
        'docty': 'doc_type',
        'lang': 'language',
        'majdocty': 'majdoctype',
        'count': 'country'
    }

    normalized_data = normalized_data.rename(columns=rename_cols)
    try:
        normalized_data['authors'] = normalized_data['authors'].map(lambda auth: auth.get('authr') if pd.notna(auth) else auth)
    except KeyError:
        # This means that the metadata doesn't have an author field
        normalized_data['authors'] = None

    # Assume that the `display_title` field follows a standard format: list -> dict
    normalized_data['display_title'] = normalized_data['display_title'].map(lambda dt: dt[0].get('display_title') if len(dt) else None)

    for col in normalized_data.columns:
        try:
            # Normalize line breaks for string data
            normalized_data[col] = normalize_str_col(normalized_data[col])
            normalized_data[col] = normalized_data[col].map(lambda x: collapse_array(x, '|'))
            normalized_data[col] = normalized_data[col].map(lambda x: collapse_nested_dict(x, '|'))

        except AttributeError:
            # column is not a string type
            continue

    normalized_data['majdoctype'] = make_unique_entry(normalized_data['majdoctype'])
    normalized_data['admreg'] = make_unique_entry(normalized_data['admreg'])
    normalized_data['geo_regions'] = normalized_data['geo_regions'].map(normalize_geo_regions)

    normalized_data['docyear'] = pd.to_datetime(normalized_data['docdt']).dt.year

    # existing_cols = normalized_data.columns.intersection(columns)
    # new_cols = pd.Index(set(columns).difference(normalized_data.columns))

    # normalized_data = normalized_data[existing_cols]

    # for col in new_cols:
    #     normalized_data[col] = None

    return normalized_data


METADATA_COLS = [
    'corpus', 'id', 'path_original', 'path_clean', 'filename_original', 'year',
    'major_doc_type', 'doc_type', 'author', 'collection', 'title', 'journal', 'volume',
    'date_published', 'digital_identifier', 'topics_src', 'url_pdf', 'url_txt', 'language_src',
    'adm_region', 'geo_region', 'country',

    # Not yet available at this stage...,
    # 'language_detected', 'language_score', 'tokens'

    # WB specific fields
    # 'wb_lending_instrument', 'wb_product_line', 'wb_major_theme', 'wb_theme', 'wb_sector',  # These are no longer available in the API or were renamed.
    'wb_subtopic_src', 'wb_project_id',
    # 'wb_environmental_category',
]

def build_wb_id(uid, max_len=9):
    # return f'wb_{"0"*(max_len - len(str(uid)))}{uid}'
    return f'wb_{uid}'


def standardize_metadata_fields(metadata_df):
    '''
    This method must be applied to the original metadata processed dataframe.
    This will assign the final field names.
    '''

    metadata_df = metadata_df.reset_index()
    metadata_df['uid'] = metadata_df.uid.map(build_wb_id)

    wb_core_field_map = {
        'uid': 'id',
        'docyear': 'year',
        'majdoctype': 'major_doc_type',
        'doctype': 'doc_type',
        'authors': 'author',
        'colti': 'collection',
        'display_title': 'title',
        'docdt': 'date_published',
        'docm_id': 'digital_identifier',
        'historic_topic': 'topics_src',
        'pdfurl': 'url_pdf',
        'txturl': 'url_txt',
        'language': 'language_src',
        'admreg': 'adm_region',
        'country': 'country',
        'geo_regions': 'geo_region',
    }

    wb_specific_field_map = {
        'lndinstr': 'wb_lending_instrument',
        'prdln': 'wb_product_line',
        'majtheme': 'wb_major_theme',
        'theme': 'wb_theme',
        'sectr': 'wb_sector',
        # 'envcat': 'wb_environmental_category',
        'projectid': 'wb_project_id',
        'subtopic': 'wb_subtopic_src',
    }

    wb_new_fields = ['corpus', 'path_original', 'path_clean', 'filename_original', 'journal', 'volume']

    path_original_dir = '/NLP/CORPUS/WB/TXT_ORIG'
    path_clean_dir = '/NLP/CORPUS/WB/TXT_CLEAN'

    # Perform post normalization preprocessing
    metadata_df['docdt'] = pd.to_datetime(metadata_df['docdt']).dt.date.map(str)

    # Apply final field names
    metadata_df = metadata_df.rename(columns=wb_core_field_map)
    metadata_df = metadata_df.rename(columns=wb_specific_field_map)

    for nf in wb_new_fields:
        if nf == 'corpus':
            metadata_df[nf] = 'wb'
        elif nf == 'filename_original':
            metadata_df[nf] = metadata_df.url_txt.map(lambda x: os.path.basename(x) if isinstance(x, str) else x)
        elif nf == 'path_original':
            metadata_df[nf] = metadata_df['id'].map(lambda x: f"{path_original_dir}/{x}.txt")
        elif nf == 'path_clean':
            metadata_df[nf] = metadata_df['id'].map(lambda x: f"{path_clean_dir}/{x}.txt")
        elif nf in ['journal', 'volume']:
            metadata_df[nf] = None

    metadata_df = metadata_df[METADATA_COLS]

    return metadata_df.set_index('id')


def scrape_normalize_dump_wb_data_page(scrape_params):
    metadb = DocumentDB()

    page_content = scrape_page(
        scrape_params.get('fl_params'), scrape_params.get('page'),
        limit=scrape_params.get('limit', 500), verbose=False, store_to_file=False
    )

    normalized_data = normalize_page_content(page_content, use_short_columns=True)
    metadata_df = standardize_metadata_fields(normalized_data)
    metadata_df = metadata_df.reset_index('id')
    metadata_df['_id'] = metadata_df['id']
    metadata_df = metadata_df.drop('id', axis=1)

    store_resp = metadb.store_metadata_data(metadata_df)
    return dict(page=scrape_params.get('page'), store_resp=store_resp)

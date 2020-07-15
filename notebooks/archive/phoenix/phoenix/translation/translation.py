import re
import os
import time
import json
import googletrans_client as gt
import requests.exceptions as excp
import pickle
from datetime import datetime
import pandas as pd

trans = gt.Translator()

words_with_digits = re.compile('\S*[0-9]+\S*')
truncate_newline = re.compile('\n+')
truncate_spaces = re.compile('[^\S\r\n]+')
remove_chars = re.compile('[«»]+')


def trim_pipeline(text):
    text = truncate_newline.sub('\n', text)
    text = truncate_spaces.sub(' ', text)

    # text = text.replace('“', '').replace('”', '')

    return text.strip()


def partition_large_dataset(dataset, col='trimmed', col_index='uri', limit=8000, split_char='\n', zfill=2):
    partitioned_dataset = {}

    for index, row in dataset.iterrows():
        trimmed = row[col]
        splits = trimmed.split(split_char)
        split_len = len(splits)

        temp_text = ''
        part = 1
        for s in splits:
            s = s.strip()

            if len(temp_text) < limit:
                ttemp_text = split_char.join([temp_text, s])
                if split_char != '\n':
                    # Do this for backward compatibility since we've downloaded without lstrip using the `\n` split_char
                    ttemp_text = ttemp_text.lstrip(split_char)

            if len(ttemp_text) > limit:
                partitioned_dataset[f'{index}__{str(part).zfill(zfill)}'] = temp_text.strip()
                temp_text = s
                part += 1
            else:
                temp_text = ttemp_text

        if temp_text.strip():
            partitioned_dataset[f'{index}__{str(part).zfill(zfill)}'] = temp_text.strip()

    partitioned_dataset = pd.DataFrame(partitioned_dataset.items(), columns=[col_index, col]).set_index(col_index)

    return partitioned_dataset


def consolidate_partitions(dataset, part_join, part_link='__'):
    return dataset.groupby(
        dataset.index.map(
            lambda x: part_link.join(x.split(part_link)[:-1])
        )
    )['trans'].apply(
        lambda x: part_join.join(x.sort_index().tolist())
    ).to_frame()


def translate_dataset(dataset, doc_size, data_dir, fname_prefix, replace_index=False, col='trimmed', src='uz', dest='en', limit=8000, batch_size=30, sleep_rate=2):
    '''
    doc_size: ['small', 'large']
    data_dir: ['small_translations', 'large_translations']
    fname_prefix: `large_partitioned_whitespace_trimmed` or `small_whitespace_trimmed`
    '''
    assert(doc_size in data_dir)
    assert(doc_size in fname_prefix)

    try:
        retry_indices
    except NameError:
        raise ValueError('`retry_indices` not defined!')

    trans = gt.Translator()
    full_tfd = pd.DataFrame()
    recover = False
    log_fname = f'{doc_size}.log'
    notify(log_fname, 'Starting this translation session...')

    for ix, ppp in enumerate(np.array_split(dataset, dataset.shape[0] // batch_size)):
        # Make sure we only include those that satisfy the limit!
        ppp[col] = ppp[col].map(lambda x: remove_chars.sub('', x))
        pp = ppp[ppp.trimmed.map(len) < limit]

        fname = os.path.join(data_dir,  f'{fname_prefix}_split_{str(ix).zfill(3)}.pickle')

        if os.path.isfile(fname):
            try:
                tdf = pd.read_pickle(fname)

                if replace_index:
                    tdf.index = pp.index
                    tdf.to_pickle(fname)

                if full_tfd.empty:
                    full_tfd = tdf
                else:
                    full_tfd = pd.concat([full_tfd, tdf])
                notify(log_fname, f'Part {ix} already translated...')
                continue

            except pickle.UnpicklingError:
                notify(log_fname, f'Redownload {ix}...')
                pass

        notify(log_fname, (ix, pp.shape))

        # First try
        try:
            translations = trans.translate(pp.trimmed.tolist(), src=src, dest=dest)
            recover = False
        except (json.JSONDecodeError, excp.ConnectionError) as e:
            notify(log_fname, f'Error {e} for {ix}, recovering...')
            recover = True

        # Try to recover
        if recover:
            payload = recover_trans(ix, pp, log_fname=log_fname, recover_num=5, src=src, dest=dest)
            translations = payload['translations']
            trans = payload['trans']

            if not translations:
                retry_indices.update(pp.index)
                continue

        tdf = pd.DataFrame([tr.text for tr in translations], columns=['trans'], index=pp.index)
        tdf.to_pickle(fname)

        if full_tfd.empty:
            full_tfd = tdf
        else:
            full_tfd = pd.concat([full_tfd, tdf])

        time.sleep(min(np.random.exponential(sleep_rate), sleep_rate))

    full_tfd.to_pickle(os.path.join(data_dir, f'{fname_prefix}_full.pickle'))

    return full_tfd


def recover_trans(ix, pp, log_fname, src='uz', dest='en', recover_num=5):
    translations = []

    for i in range(recover_num):
        trans = gt.Translator()
        notify(log_fname, f'Retry # {i + 1}...')

        try:
            translations = trans.translate(pp.trimmed.tolist(), src=src, dest=dest)
            break
        except (json.JSONDecodeError, excp.ConnectionError) as e:
            notify(log_fname, f'{e}')
            continue

        time.sleep(1)

    if not translations:
        notify(log_fname, f'Skipping {ix}...')
        trans = gt.Translator()

    return dict(
        translations=translations,
        trans=trans
    )


def notify(fname=None, message='', verbose=True):
    message = f'{datetime.now()}: {message}'

    if fname is not None:
        with open(fname, 'a+') as fl:
            fl.write(message + '\n')

    if verbose:
        print(message)
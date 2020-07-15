from phoenix.celery import celery_app
from phoenix.cleaner.cleaner import Cleaner
from phoenix.dataset.document import DocumentDB
import os
import pandas as pd
import time


@celery_app.task(
    name='phoenix.tasks.wb_nlp_tasks.clean_text',
    # autoretry_for=(Exception,),
    # retry_kwargs={'max_retries': 1}
)
def clean_text(text, ignore_length=100, use_spacy=True):
    start_time = time.time()
    tasks_path = os.path.dirname(os.path.abspath(__file__))  # phoenix/tasks
    phoenix_path = os.path.dirname(
        tasks_path
    )  # phoenix

    cleaner = Cleaner(
        use_spellchecker=True, use_respeller=True, use_lemmatizer=True,
        use_spacy=use_spacy, ignore_length=ignore_length,
        replacements_plurals_to_singular_file=os.path.join(
            phoenix_path, 'whitelists/whitelist_replacements_plurals_to_singular.csv'
        ), acronyms_file=os.path.join(
            phoenix_path, 'whitelists/whitelist_acronyms.csv'
        ),
    )

    payload = cleaner.clean_text(text)
    total_time = time.time() - start_time
    payload['total_clean_time'] = total_time

    return payload


@celery_app.task(
    name='phoenix.tasks.wb_nlp_tasks.clean_doc',
    # autoretry_for=(Exception,),
    # retry_kwargs={'max_retries': 1}
)
def clean_doc(doc_name='11758940.txt', use_spacy=True):
    start_time = time.time()
    # path = './' # /home/avsolatorio/WBG/NLP/WB/CORPUS/RAW/eap_files'
    docdb = DocumentDB()

    doc_path = '/raw_files'
    tasks_path = os.path.dirname(os.path.abspath(__file__))  # phoenix/tasks
    phoenix_path = os.path.dirname(
        tasks_path
    )  # phoenix

    fname = os.path.join(doc_path, doc_name)

    cleaner = Cleaner(
        use_spellchecker=True, use_respeller=True, use_lemmatizer=True, use_spacy=use_spacy,
        replacements_plurals_to_singular_file=os.path.join(
            phoenix_path, 'whitelists/whitelist_replacements_plurals_to_singular.csv'
        ), acronyms_file=os.path.join(
            phoenix_path, 'whitelists/whitelist_acronyms.csv'
        ),
    )

    with open(fname, 'rb') as fl:
        text = fl.read()
        text = text.decode('utf-8', errors='ignore')

    cleaned = cleaner.clean_text(text)

    doc = pd.DataFrame([cleaned])
    doc['_id'] = f'wb_{doc_name.rstrip(".txt")}'
    db_status = docdb.store_clean_docs_data(doc)
    total_time = time.time() - start_time
    db_status['total_time'] = total_time

    return db_status

from celery import Celery
import random
from phoenix.optimizers import cache_utils
from phoenix.cleaner.cleaner import Cleaner

redis = cache_utils.get_redis()

redis_host = redis.connection_pool.connection_kwargs['host']
redis_port = redis.connection_pool.connection_kwargs['port']
redis_db = redis.connection_pool.connection_kwargs['db']
redis_url = f'redis://{redis_host}:{redis_port}/{redis_db}'
redis_hash_bucket = 'celery-test'

app = Celery('tasks', broker=redis_url, backend=redis_url)


def get_from_bucket(bucket_id, key):
    return redis.hget(bucket_id, key)


@cache_utils.redis_cacher
def compute_squared(x, **kwargs):
    print('Not from cache!')
    return x**2


@app.task(name='phoenix.optimizers.celery_task.read_and_store')
def read_and_store():
    d = random.randint(0, 100)
    sq = compute_squared(d, argument_hash=d)
    return d, cache_utils.store_to_bucket(redis_hash_bucket, d, sq)


@app.task(name='phoenix.optimizers.celery_task.clean_doc')
def clean_doc(doc_name='11758940.txt', use_spacy=True):
    import os
    # path = './' # /home/avsolatorio/WBG/NLP/WB/CORPUS/RAW/eap_files'
    doc_path = '/raw_files'
    optimizers_path = os.path.dirname(os.path.abspath(__file__))  # phoenix/optimizers
    phoenix_path = os.path.dirname(
        optimizers_path
    ) # phoenix

    fname = os.path.join(doc_path, doc_name)

    cleaner = Cleaner(
        use_spellchecker=True, use_respeller=True, use_lemmatizer=True, use_spacy=use_spacy,
        replacements_plurals_to_singular_file=os.path.join(phoenix_path, 'whitelists/whitelist_replacements_plurals_to_singular.csv'),
        acronyms_file=os.path.join(phoenix_path, 'whitelists/whitelist_acronyms.csv'),
    )

    with open(fname, 'rb') as fl:
        text = fl.read()
        text = text.decode('utf-8', errors='ignore')

    cleaned = cleaner.clean_text(text)
    return cleaned

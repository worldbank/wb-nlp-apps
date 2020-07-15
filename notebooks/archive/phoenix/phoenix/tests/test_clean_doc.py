from phoenix.tasks import wb_nlp_tasks as ct
from phoenix.dataset import document
import random
import glob
import time


def process_docs(N=100):
    files = glob.glob('/home/avsolatorio/WBG/NLP/WB/CORPUS/RAW/eap_files/*.txt')

    doc_names = [random.choice(files).split('/')[-1] for _ in range(N)]
    async_objs = {i:ct.clean_doc.delay(i) for i in doc_names}
    return async_objs


def is_completed(async_objs, N):
    return len([i for i, j in async_objs.items() if j.status == 'SUCCESS']) == N


if __name__ == '__main__':
    N = 100
    start = time.time()
    async_objs = process_docs(N)
    while not is_completed(async_objs, N):
        time.sleep(1)
    total_seconds = time.time() - start

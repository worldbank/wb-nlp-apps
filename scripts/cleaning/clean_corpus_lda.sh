python -u ./scripts/cleaning/clean_corpus.py --config ./configs/cleaning/lda.yml --input-dir /data/wb536061/wb_nlp/data/raw/CORPUS --output-dir-name TXT_LDA --recursive -vv |& tee ./logs/clean_corpus.py.lda.log
# python -u ./scripts/cleaning/clean_corpus.py --config ./configs/cleaning/lda.yml --input-dir ./data/raw --output-dir-name TXT_LDA --recursive -vv |& tee ./logs/clean_corpus.py.lda.log

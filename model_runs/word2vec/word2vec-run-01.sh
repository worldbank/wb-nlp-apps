MODEL_CONFIG_ID=702984027cfedde344961b8b9461bfd3
CLEANING_CONFIG_ID=229abf370f281efa7c9f3c4ddc20159d
DESCRIPTION="Word2vec D100 W5 N5 SG Full Corpus"

# D100: 100 dimensions
# W5:   window = 5
# N5:   negative sample = 5
# SG:   skip-gram

python -u ./scripts/models/train_word2vec_base_model.py --model-config-id ${MODEL_CONFIG_ID} --cleaning-config-id ${CLEANING_CONFIG_ID} --description "${DESCRIPTION}" -vv |& tee ./data/logs/train_word2vec_base_model.py.`basename "$0"`.`date +%Y-%m-%d+%H:%M:%S`.log

MODEL_CONFIG_ID=ef0ab0459e9c28de8657f3c4f5b2cd86
CLEANING_CONFIG_ID=c6839bba558fb72b1c03089b1add98b8
DESCRIPTION="LDA topic model with 75 topics - full corpus"

python -u ./scripts/models/train_lda_base_model.py --model-config-id ${MODEL_CONFIG_ID} --cleaning-config-id ${CLEANING_CONFIG_ID} --description "${DESCRIPTION}" -vv |& tee ./data/logs/train_lda_base_model.py.`basename "$0"`.log

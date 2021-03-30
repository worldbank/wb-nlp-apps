MODEL_CONFIG_ID=5e26b5090bdd91d7aee4e5e89753a33b
CLEANING_CONFIG_ID=c6839bba558fb72b1c03089b1add98b8
DESCRIPTION="Mallet LDA topic model with 75 topics - full corpus"

python -u ./scripts/models/train_mallet_base_model.py --model-config-id ${MODEL_CONFIG_ID} --cleaning-config-id ${CLEANING_CONFIG_ID} --description "${DESCRIPTION}" -vv |& tee ./data/logs/train_mallet_base_model.py.`basename "$0"`.log

from flask_restful import Resource, reqparse
from services.data_cleaner_module import Cleaner

from services.ngrams import NGramMapper
import werkzeug

from wb_nlp.dir_manager import get_data_dir


parser = reqparse.RequestParser()
parser.add_argument(
    'raw_text', type=str,
    required=True, help='raw text input required'
)
parser.add_argument(
    'file', type=werkzeug.datastructures.FileStorage,
    location='files',
    required=False, help='File to upload.'
)

cleaner = Cleaner(
    use_spellchecker=True, use_respeller=True, use_lemmatizer=True, use_spacy=True,
    replacements_plurals_to_singular_file=get_data_dir(
        'whitelists', 'whitelists', 'whitelist_replacements_plurals_to_singular.csv'),
    acronyms_file=get_data_dir(
        'whitelists', 'whitelists', 'whitelist_acronyms.csv'),
    ignore_length=0,
    check_language=False,
)

ngrams = NGramMapper(
    whitelist_file=get_data_dir(
        'whitelists', 'whitelists', 'whitelist_ngrams_cleaned.csv')  # '../SCRIPTS/whitelists/whitelist_ngrams_truncated_cleaned.csv'
)


def clean_text(text):
    data = cleaner.clean_text(text)
    data['ngram_text'] = ngrams.replace_ngrams(data['text'])

    # data['text'] = text
    # data['ngram_text'] = text

    return data


class CleanText(Resource):
    def post(self):
        args = parser.parse_args()

        if args.get('file') is not None:
            file = args['file']
            text = file.read()
            try:
                text = text.decode('utf-8', 'ignore')
            except:
                return {'Error': "File can't be decoded."}

        elif args.get('raw_text') is not None:
            text = args['raw_text']
        else:
            return {'Error': 'Please provide a file or a raw_text parameter.'}

        return clean_text(text)

    def get(self):
        return self.post()

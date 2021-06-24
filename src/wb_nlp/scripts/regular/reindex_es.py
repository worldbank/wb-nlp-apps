from elasticsearch_dsl import Index
from wb_nlp.interfaces import elasticsearch, mongodb


def reindex_es(ignore_existing=False, en_txt_only=True, remove_doc_whitespaces=True, delete_index=False):
    if delete_index:
        print("Deleting index...")
        i = Index(name=elasticsearch.DOC_INDEX,
                  using=elasticsearch.get_client())
        i.delete()
        elasticsearch.NLPDoc.init()

    docs_metadata_coll = mongodb.get_collection(
        db_name="test_nlp", collection_name="docs_metadata")
    docs_metadata = list(docs_metadata_coll.find({}))

    print(f"Found {len(docs_metadata)}...")

    elasticsearch.make_nlp_docs_from_docs_metadata(
        docs_metadata, ignore_existing=ignore_existing, en_txt_only=en_txt_only, remove_doc_whitespaces=remove_doc_whitespaces)


def main(ignore_existing=False, en_txt_only=True, remove_doc_whitespaces=True, delete_index=False):
    reindex_es(ignore_existing=ignore_existing, en_txt_only=en_txt_only,
               remove_doc_whitespaces=remove_doc_whitespaces, delete_index=delete_index)


if __name__ == "__main__":
    import argparse

    def boolean_string(s):
        if s not in {'False', 'True'}:
            raise ValueError('Not a valid boolean string')
        return s == 'True'

    parser = argparse.ArgumentParser()

    parser.add_argument('--ignore-existing', dest='ignore_existing',
                        type=boolean_string, default=False)

    parser.add_argument('--en-txt-only', dest='en_txt_only',
                        type=boolean_string, default=True)

    parser.add_argument('--remove-doc-whitespaces', dest='remove_doc_whitespaces',
                        type=boolean_string, default=True)

    parser.add_argument('--delete-index', dest='delete_index',
                        type=boolean_string, default=False)

    args = parser.parse_args()
    print(args)

    main(**vars(args))

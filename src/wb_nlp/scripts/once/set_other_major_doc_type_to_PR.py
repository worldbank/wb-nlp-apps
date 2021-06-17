import elasticsearch_dsl
from wb_nlp.interfaces import elasticsearch


def set_other_wb_maj_doc_type_to_PR():
    other_types = ["Evaluation Document",
                   "Country Focus", "Economic and Sector Work", "Publications and Research"]
    ids = elasticsearch.get_ids_from_query(
        elasticsearch.NLPDoc,
        query=elasticsearch.NLPDoc.search().filter(
            "terms", major_doc_type=other_types).to_dict()["query"],

        ids_only=True
    )
    ids = list(ids)

    if ids:
        print(f"Updating major_doc_type for {len(ids)} documents...")

        ubq = elasticsearch_dsl.UpdateByQuery(
            index=elasticsearch.NLPDoc.Index.name, using=elasticsearch.get_client())
        ubq = ubq.filter("terms", id=ids)
        ubq = ubq.script(
            source='ctx._source.major_doc_type=["Publications and Reports"];')
        ubq = ubq.params(scroll_size=50).params(
            conflicts="proceed")  # .params(requests_per_second=10)

        print("Executing major doc type update...")
        response = ubq.execute()
        print(response.to_dict())
    else:
        print("No ids that need updating...")


def main():
    set_other_wb_maj_doc_type_to_PR()


if __name__ == "__main__":

    main()

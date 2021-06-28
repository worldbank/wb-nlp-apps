import elasticsearch_dsl
from wb_nlp.interfaces import mongodb, elasticsearch


def sync_doc_topic_metadata():

    doc_topic_meta_fields = [
        "id",
        "adm_region", "country", "corpus", "date_published",
        # "der_acronyms",
        "der_country", "der_jdc_tags", "der_regions",
        "doc_type", "geo_region", "major_doc_type", "topics_src", "year"]

    collection = mongodb.get_es_nlp_doc_metadata_collection()
    metadata = list(collection.find({}, projection=doc_topic_meta_fields))
    num_items = len(metadata)

    print(f"Processing {num_items} items...")

    for ix, meta in enumerate(metadata):
        ubq = elasticsearch_dsl.UpdateByQuery(
            index=elasticsearch.DocTopic.Index.name, using=elasticsearch.get_client())
        ubq = ubq.filter("term", id=meta["id"])
        ubq = ubq.script(
            source="""
            ctx._source.adm_region=params.adm_region;
            ctx._source.country=params.country;
            ctx._source.corpus=params.corpus;
            ctx._source.date_published=params.date_published;
            ctx._source.der_country=params.der_country;
            ctx._source.der_jdc_tags=params.der_jdc_tags;
            ctx._source.der_regions=params.der_regions;
            ctx._source.doc_type=params.doc_type;
            ctx._source.geo_region=params.geo_region;
            ctx._source.major_doc_type=params.major_doc_type;
            ctx._source.topics_src=params.topics_src;
            ctx._source.year=params.year;
            """,
            params=meta)
        ubq = ubq.params(scroll_size=50).params(
            conflicts="proceed")  # .params(requests_per_second=10)

        response = ubq.execute()
        print(f"{ix + 1} / {num_items}",
              meta["corpus"], meta["id"], response.to_dict())


def main():
    sync_doc_topic_metadata()


if __name__ == "__main__":

    main()

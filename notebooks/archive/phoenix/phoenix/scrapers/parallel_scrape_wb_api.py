from phoenix.scrapers import wb_metadata_scraper as wms
# from phoenix.dataset import document

# metadb = document.DocumentDB()
# coll = metadb.get_metadata_collection()
# ids = len([i['_id'] for i in coll.find(filter={}, projection=['_id'])])

meta_async_objs = wms.scrape_worldbank_operational_docs_api(fl_params=wms.fl_params, limit=100, max_pages=None, to_celery=True)

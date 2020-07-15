from phoenix.celery import celery_app
from phoenix.scrapers.wb_metadata_scraper import scrape_normalize_dump_wb_data_page
import os
import pandas as pd


@celery_app.task(
    name='phoenix.tasks.wb_metadata_scraper_tasks.scrape_and_store_page',
    # autoretry_for=(Exception,),
    # retry_kwargs={'max_retries': 1}
)
def scrape_and_store_page(scrape_params):
    return scrape_normalize_dump_wb_data_page(scrape_params)

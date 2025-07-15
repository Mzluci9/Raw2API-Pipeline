from dagster import job, op, ScheduleDefinition, get_dagster_logger
import subprocess
import os
from pathlib import Path

@op
def scrape_telegram(context):
    logger = get_dagster_logger()
    result = subprocess.run(["python", "src/scraping/telegram_scraper.py"], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Scrape failed: {result.stderr}")
        raise Exception("Scrape failed")
    logger.info("Telegram scrape complete")
    return True

@op
def load_to_postgres(context, scrape_success):
    logger = get_dagster_logger()
    if not scrape_success:
        raise Exception("Skipping load due to scrape failure")
    result = subprocess.run(["python", "src/scraping/load_to_postgres.py"], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Load failed: {result.stderr}")
        raise Exception("Load failed")
    logger.info("Load to PostgreSQL complete")
    return True

@op
def run_dbt(context, load_success):
    logger = get_dagster_logger()
    if not load_success:
        raise Exception("Skipping dbt due to load failure")
    os.chdir("dbt/tenx_dbt")
    result = subprocess.run(["dbt", "run"], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"dbt run failed: {result.stderr}")
        raise Exception("dbt run failed")
    logger.info("dbt run complete")
    return True

@op
def process_images(context, dbt_success):
    logger = get_dagster_logger()
    if not dbt_success:
        raise Exception("Skipping image processing due to dbt failure")
    result = subprocess.run(["python", "src/enrichment/process_images.py"], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Image processing failed: {result.stderr}")
        raise Exception("Image processing failed")
    logger.info("Image processing complete")
    return True

@job
def tenx_pipeline():
    scrape_success = scrape_telegram()
    load_success = load_to_postgres(scrape_success)
    dbt_success = run_dbt(load_success)
    process_images(dbt_success)

# Schedule to run daily at 1 AM
schedule = ScheduleDefinition(
    job=tenx_pipeline,
    cron_schedule="0 1 * * *"
)
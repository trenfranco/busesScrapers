import json
from database.data_validator import validate_scraped_data
from database.populate_db import populate_db
from scraper.pdf_to_html import convert_pdf_to_html_tables
from scraper.download_pdf import download_pdf
from scraper.microbird_scraper import microbird_scraper
import os


def main():

    # Download pdf
    download_pdf()

    pdf_folder = "./data"

    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

    # Iterates by every file
    for idx, pdf_path in enumerate(pdf_files):
        convert_pdf_to_html_tables(pdf_path, idx)

    # Scrape data and store 
    json_file = microbird_scraper()

    # Validate data
    validated_buses = validate_scraped_data(json_file)

    # Save the validated data
    with open("data/validated_buses_microbird.json", "w", encoding="utf-8") as f:
        json.dump(validated_buses, f, indent=4, ensure_ascii=False)
    validated_file = "data/validated_buses_microbird.json"

    # Populate DB
    populate_db(validated_file)


if __name__ == "__main__":
    main()

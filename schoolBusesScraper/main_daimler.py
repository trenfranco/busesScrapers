import json
from database.data_validator import validate_scraped_data
from database.populate_db import populate_db
from scraper.daimler_scraper import daimler_scraper


def main():

    # Scraoe data and store 
    json_file = daimler_scraper()

    # Validate data
    validated_buses = validate_scraped_data(json_file)

    # Save the validated data
    with open("data/validated_buses_daimler.json", "w", encoding="utf-8") as f:
        json.dump(validated_buses, f, indent=4, ensure_ascii=False)
    validated_file = "data/validated_buses_daimler.json"

    # Populate DB
    populate_db(validated_file)

    


if __name__ == "__main__":
    main()

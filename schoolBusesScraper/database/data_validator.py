import json


def validate_scraped_data(scraped_data):
    """
    Validates scraped JSON data against the expected database schema
    return: List of validated buses, List of errors
    """
    validated_data = []
    errors = []

    # Expected schema
    expected_schema = {
        "title": str,
        "year": str,
        "make": str,
        "model": str,
        "engine": (str, type(None)),
        "transmission": (str, type(None)),
        "mileage": (str, type(None)),
        "passengers": (str, type(None)),
        "wheelchair": str,
        "price": (str, type(None)),
        "vin": (str, type(None)),
        "images": list,
        "location": (str, type(None)),
        "description": (str, type(None)),
        "features": (str, type(None)),
        "image_url": (str, type(None))
    }

    # Data type lengths
    max_length = {
        "title": 256,
        "year": 10,
        "make": 25,
        "model": 50,
        "engine": 60,
        "transmission": 60,
        "mileage": 100,
        "passengers": 60,
        "wheelchair": 60,
        "price": 30,
        "vin": 60,
        "location": 30
    }

    for index, bus in enumerate(scraped_data):
        validation_errors = []
        validated_bus = {}

        for field, expected_type in expected_schema.items():
            value = bus.get(field)

            # Validate field type
            if not isinstance(value, expected_type):
                (validation_errors.append
                 (f"{field} incorrect type. Expected {expected_type}, "
                  f"got {type(value)}"))
                value = None  # Default to None if invalid

            # Trim long strings
            if isinstance(value, str) and field in max_length:
                value = value[:max_length[field]]

            validated_bus[field] = value

        # Validate images list
        if "images" in bus and isinstance(bus["images"], list):
            validated_bus["images"] = ([str(img)[:1000]
                                        for img in bus["images"]
                                        if isinstance(img, str)])
        else:
            validated_bus["images"] = []

        if validation_errors:
            errors.append({"bus_index": index, "errors": validation_errors})

        validated_data.append(validated_bus)

    return validated_data, errors


# Load JSON and validate
with open("data/scraped_buses.json", "r", encoding="utf-8") as f:
    scraped_buses = json.load(f)

validated_buses, validation_errors = validate_scraped_data(scraped_buses)

# Save the validated data
with open("data/validated_buses.json", "w", encoding="utf-8") as f:
    json.dump(validated_buses, f, indent=4, ensure_ascii=False)

# Print errors if any
if validation_errors:
    print("There are some validation errors:")
    for error in validation_errors:
        print(f"Bus Index {error['bus_index']}: {error['errors']}")
else:
    print("The JSON file is valid and saved to validated_buses.json!")

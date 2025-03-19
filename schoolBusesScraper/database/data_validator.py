import json


def validate_scraped_data(json_data):
    """
    Validates scraped JSON data against the expected database schema
    return: List of validated buses, List of errors
    """
    # Load JSON and validate
    with open(json_data, "r", encoding="utf-8") as f:
        scraped_data = json.load(f)

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
        "brake": (str, type(None)),
        "color": (str, type(None)),
        "source_url": (str, type(None)),
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
        "location": 30,
        "brake": 30,
        "color": 60,
        "source_url": 1000,
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

    # Print errors if any
    if validation_errors:
        print("There are some validation errors:")
        for error in validation_errors:
            print(f"Bus Index {error['bus_index']}: {error['errors']}")
    else:
        print("The JSON file is valid and saved to validated_buses.json!")

    return validated_data
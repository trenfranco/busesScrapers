import json
import pymysql
from database.db_config import get_connection


def populate_db(json_file):
    """"
    Test DB connetcion and use a
    validated json to populate the DB
    """

    # Load validated JSON
    with open(json_file, "r", encoding="utf-8") as f:
        buses_data = json.load(f)

    # Connect to MySQL
    conn = get_connection()
    cursor = conn.cursor()

    # Insert data
    for bus in buses_data:
        try:
            # Checks for duplicate using VIN number
            cursor.execute("SELECT id FROM buses WHERE vin = %s", (bus.get("vin"),))
            existing_bus = cursor.fetchone()

            if existing_bus:
                bus_id = existing_bus["id"]
            else:
                # Insert into the table: buses 
                cursor.execute("""
                    INSERT INTO buses 
                    (title, make, model, year, mileage, passengers, wheelchair, price, vin, engine, transmission, 
                    location, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    bus.get("title"), bus.get("make"), bus.get("model"), bus.get("year"), bus.get("mileage"), 
                    bus.get("passengers"), bus.get("wheelchair"), bus.get("price"), bus.get("vin"), 
                    bus.get("engine"), bus.get("transmission"), bus.get("location"), bus.get("description")
                ))
                bus_id = cursor.lastrowid  # Get the last inserted ID

                # Insert into the table: buses_overview
                cursor.execute("""
                    INSERT INTO buses_overview 
                    (bus_id, mdesc, intdesc, extdesc, features, specs)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    bus_id, bus.get("description"), None, None, bus.get("features"), None
                ))

            # Insert into the table: buses_images
            if isinstance(bus.get("images"), list):  # Ensure images is a list
                for i, img_url in enumerate(bus.get("images", [])):
                    img_url_cleaned = img_url.strip('"').strip('\\')
                    cursor.execute("""
                        INSERT INTO buses_images (name, url, image_index, bus_id)
                        VALUES (%s, %s, %s, %s)
                    """, (f"Image {i+1}", img_url_cleaned, i, bus_id))

            conn.commit()
            print(f"Inserted Bus VIN: {bus.get('vin')})")

        except Exception as e:
            conn.rollback()  # Undo changes
            print(f"Error inserting bus VIN: {bus.get('vin')}: {e}")

    # Close connection
    cursor.close()
    conn.close()

    print("Database populated!")

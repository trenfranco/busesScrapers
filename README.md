# Bus Scraper & Database Pipeline 🚌

## **Project summary**
This project automates the **scraping, validation, and database storage** of bus listings from multiple sources. It uses **Selenium for web scraping**, **MySQL for data storage**, and follows a structured **ETL (Extract, Transform, Load) pipeline**. Depending on the scraper script, it scrapes dinamycally or just in HTML parser mode.

## **Project Structure**
├── data/ │ ├── empty.json │ <br>├── database/ │├── data_validator.py │├── db_config.py │ ├── db_setup.sql │ ├── populate_db.py │ <br>├── scraper/ │├── daimler_scraper.py │ ├── download_pdf.py │ ├── rossbus_scraper.py │ <br>├── main_daimler.py  <br>├── main_microbird.py <br> ├── main_rossbus.py  <br>├── requirements.txt
 <br>
 <br>
 **database** folder contains scritps to validate, transform and load the data. Also some scripts to connect and setup the DB schema.
 <br> <br>
  **scraper** folder contains the python web scrapers to extract data as a csv files, which are going to be stored inside **data** folder, which stores the scraped and validated **JSON**s and **PDF** files
 <br> <br>
 The **main** python files execute the entire **ETL** process for each website scraped.
 <br>
  ## **Data flow**
  Firstly, any **main_.py** file is executed depending whch site you want to scrape, one of the three **scraper_.py** files scrapes the website and then an unvalidated JSON file is created inside **data folder**, then **data_validator.py** script validates types and restrictions following the DBs schemas, creating another JSON file but **validated**.<br>
  Finally the **populate_db.py** script is called to load the extracted and validated data to our tables, managing **duplicated** items.
 ## **Requirements**
 -Google chrome, MySQL and python 3.8+
## **How to run**
<br>
Run:
<br>
pip install selenium
<br>
pip install webdriver-manager
<br>
pip install pymysql
<br>
pip install pandas
<br>
pip install pdfplumber
<br>
python -m venv venv<br>
source venv/bin/activate  # Mac/Linux<br>
venv\Scripts\activate     # Windows<br>
pip install -r requirements.txt<br>
<br>
To create DB schema execute **db_setup.sql** script.
<br>
Modify **db_config.py** values for your specidic DB.
<br><br>
**Finally run any of the main files**

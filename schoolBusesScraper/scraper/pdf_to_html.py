import pdfplumber
import pandas as pd


def convert_pdf_to_html_tables(pdf_path, html_name):

    html_tables = []

    # Open and extract tables
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_tables = page.extract_tables()
            for table in extracted_tables:
                df = pd.DataFrame(table)
                html_tables.append(df.to_html(index=False, escape=False))  # Convert to HTML

    # Save the needed table
    for idx, html in enumerate(html_tables):
        if idx == 2:
            html_filename = f"./data/table_{html_name}.html"
            with open(html_filename, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Table {idx+1} saved in {html_filename}")

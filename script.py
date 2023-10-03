import requests
import pandas as pd
from openpyxl import Workbook
from bs4 import BeautifulSoup

"""
1) Identificar correctamente el elemento(s) que contienen 
informacion deseada
 

"""
# Define the URL of the CSV file to download
web_page_url = "https://www.suseso.cl/608/w3-article-708568.html"

# Send an HTTP GET request to the web page
response = requests.get(web_page_url)



























"""
    if response.status_code == 200:
        # Read the CSV data into a DataFrame
        df = pd.read_csv(pd.compat.StringIO(response.text))
        
        # Create an XLSX writer
        writer = pd.ExcelWriter(output_path, engine='openpyxl')
        writer.book = Workbook()
        
        # Write the DataFrame to an XLSX sheet
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        writer.close()
        print("CSV file successfully transformed to XLSX.")
    else:
        print("Failed to download the CSV file.")

# Loop through Excel sheets
for sheet_number in range(1, 41):  # Assuming 40 sheets
    # Load the Excel sheet using openpyxl or another library
    sheet = load_excel_sheet(sheet_number)
    
    # Process the sheet data as needed (e.g., extract specific data)
    extracted_data = process_excel_sheet(sheet)
    
    # Define the output path for the XLSX file
    output_path = f"output_data/sheet_{sheet_number}.xlsx"
    
    # Save the extracted data to an XLSX file
    download_csv_and_transform_to_xlsx(extracted_data, output_path)
"""
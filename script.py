import requests
import pandas as pd
import os
from openpyxl import Workbook
from bs4 import BeautifulSoup
from urllib.parse import urljoin
"""
1) Identificar correctamente el elemento(s) que contienen 
informacion deseada
   Elemento general: 
    <div id="article_i__ss_ar_articulo_archivos_1" class="recuadros download-attr margen-abajo-md"><div class="recuadro format-pdf externo cid-507 aid-708568 binary-archivo_01 format-xlsx media"><a href="articles-708568_archivo_01.xlsx" title="Ir a Estadísticas de la Seguridad Social 2022" download="Estadísticas de la Seguridad Social 2022.pdf">Estadísticas de la Seguridad Social 2022</a></div></div>
 Especificamete:
    div que contiene el link de descarga > article_i__ss_ar_articulo_archivos_1
    <a href="articles-708568_archivo_01.xlsx" title="Ir a Estadísticas de la Seguridad Social 2022" download="Estadísticas de la Seguridad Social 2022.pdf">Estadísticas de la Seguridad Social 2022</a>

"""
web_page_url = "https://www.suseso.cl/608/w3-article-708568.html"

response = requests.get(web_page_url)

soup = BeautifulSoup(response.text, 'lxml') 

downloadDir = os.path.join(os.getcwd(), "downloadedFiles")
os.makedirs(downloadDir, exist_ok=True)

for a_tag in soup.find_all('a'):
    if a_tag.get("href") == "articles-708568_archivo_01.xlsx" and a_tag.get("title") == "Ir a EstadÃ­sticas de la Seguridad Social 2022":
        downloadUrl = "https://www.suseso.cl/608/articles-708568_archivo_01.xlsx"
        fileName = os.path.basename(downloadUrl)
        localPath = os.path.join(downloadDir, fileName)
        fileResponse = requests.get(downloadUrl)

        if fileResponse.status_code == 200:
            with open(localPath, "wb") as localFile:
                localFile.write(fileResponse.content)
            print(f"{localPath} descargado correctamente")
        else:
            print("No funciono")


     






























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
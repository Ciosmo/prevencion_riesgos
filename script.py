import requests
import pandas as pd
import os
import openpyxl
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
            #testing
            workbookv2 = openpyxl.load_workbook(localPath)
            ws = workbookv2.active
            print(ws)
            wantedSheet = '31'
            
            if wantedSheet in workbookv2.sheetnames:
                workbookv2.active = workbookv2[wantedSheet]
                ws = workbookv2.active
                print(f"switched to sheet: {ws.title}") 
                
                for row in ws.iter_rows():
                    for cell in row:
                        print(f"cell {cell.coordinate}: {cell.value}" )
                print(f"additional information: this is sheet '{wantedSheet}'")
            else:
                print(f"sheet {wantedSheet} not found in woorkbook")
            """
            sheetIdx = 31
            if sheetIdx < len(workbookv2.sheetnames):
                sheet = workbookv2.worksheets[sheetIdx]
                cell_value = sheet['A1'].value
                print(f"Value in cell A1 of sheet '32': {cell_value}")
            else:
                print("Invalid sheet idx")

            """           
            
            
                        
            """
            workbook = openpyxl.load_workbook(localPath) 
            SheetIdx= '31'
            refSearch = 32
            sheetIdx = workbook[SheetIdx] 
            
            for fila in sheetIdx.iter_rows(values_only=True):
                for celda in fila:
                    if str(celda.value) == refSearch:
                       NameWantedSheet = fila[1].value
                       wantedSheet = workbook[NameWantedSheet]
                       print("Nombre de la hoja deseada: ", wantedSheet.title)
                       break
            """
            
            """
            if chapter_name in workbook.sheetnames:
                chapter_sheet = workbook[chapter_name]
                if sheet_index in chapter_sheet.sheetnames
            """

            """
            Iterar por todas las hojas
            sheet= workbook.sheetnames
            for sh in sheet:
               print(sh) 
            """
            """
            chapterName = "I Régimen de Accidentes del Trabajo y Enfermedades Profesionales"
            
            extractedData = []
            
            try:
            
            except KeyError:
                print(f"La hoja {chapterName} no fue encontrada en el archivo excel ")
            """
           
        else:
            print("Didn't work")
           
           
           
           
           
           
           
           
           
           
           
            """
             #listas de hojas en el workbook
            
            sheetName = workbook.sheetnames
            for sn in sheetName:
                print(sn)
                break
            """
           
            
      
     































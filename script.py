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
                
                categoryData={
                      "ACCIDENTES DEL TRABAJO": {
                        "name_cell": 'B26',
                        "ACHS": 'C26',
                        "MUSEG": 'D26',
                        "IST": 'E26',
                        "total_cell": 'F26',
                        "economicActivityStart": 'B9',
                        "economicActivityEnd": 'B25',
                    },
                    "ACCIDENTES DE TRAYECTO": {
                        "name_cell": 'B45',
                        "ACHS": 'C45',
                        "MUSEG": 'D45',
                        "IST": 'E45',
                        "total_cell": 'F45',
                        "economicActivityStart": 'B28',
                        "economicActivityEnd": 'B44',
                    },
                    "ACCIDENTES (TRABAJO + TRAYECTO)": {
                        "name_cell": 'B64',
                        "ACHS": 'C64',
                        "MUSEG": 'D64',
                        "IST": 'E64',
                        "total_cell": 'F64',
                        "economicActivityStart": 'B47',
                        "economicActivityEnd": 'B63',
                    },
                }
                
                data = {}
                
                for category, categoryInfo in categoryData.items():
                    data[category] = {}
                    data[category]['Name'] = ws[categoryInfo['name_cell']].value
                    data[category]['Economic Activities'] = {}

                    economic_activity_start = ws[categoryInfo['economicActivityStart']]
                    economic_activity_end = ws[categoryInfo['economicActivityEnd']]
                    for row in range(economic_activity_start.row, economic_activity_end.row + 1):
                        economic_activity_cell = ws.cell(row=row, column=economic_activity_start.column)
                        economic_activity = economic_activity_cell.value
                        data[category]['Economic Activities'][economic_activity] = {}
                        for key, cell_address in categoryInfo.items():
                            if key not in ['name_cell', 'economicActivityStart', 'economicActivityEnd']:
                                cell = cell_address.replace(categoryInfo['name_cell'], economic_activity)
                                data[category]['Economic Activities'][economic_activity][key] = ws[cell].value
                        """
                        for key in categoryInfo.keys():
                            if key not in ['name_cell', 'economicActivityStart', 'economicActivityEnd']:
                               cell = categoryInfo[key].replace(categoryInfo['name_cell'], economic_activity)
                               data[category]['Economic Activities'][economic_activity][key] = ws[cell].value
                        """
                for category, categoryInfo in data.items():
                    print(f"{categoryInfo['Name']}")
                    for economicActivity, economicData in categoryInfo['Economic Activities'].items():
                        print(f"economic activity: {economicActivity}")
                        for key, value in economicData.items():
                            print(f"{key}: {value}")
                
            """   
            categories = [
                "ACCIDENTES DEL TRABAJO",
                "ACCIDENTES DE TRAYECTO",
                "ACCIDENTES (TRABAJO + TRAYECTO)"
            ]
            
            mutualities = ["ACHS", "MUSEG", "IST", "TOTAL"]
            
            data = {category: {mutuality: {} for mutuality in mutualities} for category in categories}

            
            
            categoryRanges = {
                "ACCIDENTES DEL TRABAJO": ("B9", "B25"),
                "ACCIDENTES DE TRAYECTO": ("B28", "B44"),
                "ACCIDENTES (TRABAJO + TRAYECTO)": ("B47", "B63"),
                
            }
            mutuality_column_indices = {
                "ACHS": 3,
                "MUSEG": 4,
                "IST": 5,
                "TOTAL": 6
            }
            
            for category, (start_cell, end_cell) in categoryRanges.items():
                categoryData = data[category]
                for mutuality in mutualities:
                    for row in range(2, ws.max_row + 1):
                        cellValue = ws.cell(row=row, column=mutuality_column_indices[mutuality]).value
                        if cellValue is not None:
                            categoryData[mutuality][ws.cell(row=row,column=1).value] = cellValue
            
            for category in categories:
                print(category)
                for mutuality in mutualities:
                    print(mutuality)
                    for activity, value in data[category][mutuality].items():
                        print(f"{activity}: {value}")
                    print()
            """        
            """
            categoryPositions = {
                    "ACCIDENTES DEL TRABAJO": "B8",
                    "TOTAL ACCIDENTES DEL TRABAJO": "B26",
                    "ACCIDENTES DE TRAYECTO": "B27",
                    "TOTAL ACCIDENTES DEL TRAYECTO": "B45",
                    "ACCIDENTES (TRABAJO + TRAYECTO)": "B46",
                    "TOTAL TRABAJO Y TRAYECTO": "B64",
                }
            category_positions = {
                    "ACCIDENTES DEL TRABAJO": ("B8", "B26"),
                    "ACCIDENTES DE TRAYECTO": ("B27", "B45"),
                    "TOTAL TRABAJO Y TRAYECTO": ("B46", "B64"),
                }

        
            
            if wantedSheet in workbookv2.sheetnames:
                workbookv2.active = workbookv2[wantedSheet]
                ws = workbookv2.active
                print(f"switched to sheet: {ws.title}") 
                
                interestingData = []
                currentCategory = None
               
                for category, (start_cell, end_cell)in category_positions.items():
                    currentCategory = category
                for row in ws.iter_rows(min_row=start_cell, max_row=end_cell, min_col=2, max_col=5, values_only=True):
                    for activity, achs, museg, ist, total in row:
                        interestingData.append((category, activity, achs, museg, ist, total ))
                for category, activity, achs, museg, ist, total in interestingData:
                    print(f"category {category}, actitivty {activity}, achs {achs}, museg {museg}, ist {ist}, total{total} ")    
                print(f"additional information: this is sheet {wantedSheet}")   
            else:
                print(f"sheet {wantedSheet} not found in workbook")
             
            """           
                        
                        
                        
                        
                        
                        
                        
                        
            """
                        if isinstance(cellValue, (int, float)):
                            textValue = None
                            cellIdx = row.index(cellValue)
                            if cellIdx > 0:
                                textValue = row[cellIdx - 1]
                                
                            if textValue is not None and isinstance(textValue, str):
                                interestingData.append((textValue, cellValue))
                for text, numeric in interestingData:
                    print(f"text: {text}, numeric: {numeric}")
                
                print(f"addditional information: this is sheet {wantedSheet}")
                """
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
           
            
      
     































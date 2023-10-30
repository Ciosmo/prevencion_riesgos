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
try:
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
        
                    
                    categoryData = {
                            "ACCIDENTES DEL TRABAJO": {
                                "economicActivityStart": 'B9',
                                "economicActivityEnd": 'B26',
                                "totalColumn": 'F',
                            },
                            "ACCIDENTES DE TRAYECTO": {
                                "economicActivityStart": 'B28',
                                "economicActivityEnd": 'B45',  # Updated to 'B45'
                                "totalColumn": 'F',
                            },
                            "ACCIDENTES (TRABAJO + TRAYECTO)": {
                                "economicActivityStart": 'B48',  # Updated to 'B48'
                                "economicActivityEnd": 'B64',
                                "totalColumn": 'F',
                            },
                    }

                    data = {}

                    for category, categoryInfo in categoryData.items():
                        data[category] = {}
                        
                        economicActivityStart = ws[categoryInfo['economicActivityStart']]
                        economicActivityEnd = ws[categoryInfo['economicActivityEnd']]
                        total_column = categoryInfo['totalColumn']
                        
                        economicActivities = []
                        total_values = []
        
                        for row in range(economicActivityStart.row, economicActivityEnd.row + 1):
                            economic_activity_cell = ws.cell(row=row, column=economicActivityStart.column)
                            economic_activity = economic_activity_cell.value
                            achs_value = economic_activity_cell.offset(column=1).value
                            museg_value = economic_activity_cell.offset(column=2).value
                            ist_value = economic_activity_cell.offset(column=3).value
                            total_value = ws[f"{total_column}{row}"].value  # Fetch the "Total" from the specified column
                            
                            economicActivities.append({
                                "Economic Activity": economic_activity,
                                "ACHS": achs_value,
                                "MUSEG": museg_value,
                                "IST": ist_value,
                            })
                            total_values.append(total_value)

                        data[category]['Total'] = total_values  # Store all "Total" values for each economic activity
                        data[category]['Economic Activities'] = economicActivities

                    for category, categoryInfo in data.items():
                        print(category)
                        for i, economic_activity in enumerate(categoryInfo['Economic Activities']):
                            print(f"Economic activity: {economic_activity['Economic Activity']}")
                            print(f"ACHS: {economic_activity['ACHS']}")
                            print(f"MUSEG: {economic_activity['MUSEG']}")
                            print(f"IST: {economic_activity['IST']}")
                            print(f"Total: {categoryInfo['Total'][i]}")
                        print()
except requests.exceptions.RequestException as e:
    print(f"An error ocurrred while downloading the file: {e}") 
    
    """
                categoryData = {
                    "ACCIDENTES DEL TRABAJO": {
                        "economicActivityStart": 'B9',
                        "economicActivityEnd": 'B25',
                    },
                    "ACCIDENTES DE TRAYECTO": {
                        "economicActivityStart": 'B28',
                        "economicActivityEnd": 'B44',
                    },
                    "ACCIDENTES (TRABAJO + TRAYECTO)": {
                        "economicActivityStart": 'B47',
                        "economicActivityEnd": 'B63',
                    },
                }
                data = {}
                
                for category, categoryInfo in categoryData.items():
                    data[category] = {}
                    
                    economicActivityStart = ws[categoryInfo['economicActivityStart']]
                    economicActivityEnd = ws[categoryInfo['economicActivityEnd']]

                    economicActivities = []
                    
                    for row in range(economicActivityStart.row, economicActivityEnd.row + 1):
                        economic_activity_cell = ws.cell(row=row, column=economicActivityStart.column)
                        economic_activity = economic_activity_cell.value
                        achs_value = economic_activity_cell.offset(column=1).value
                        museg_value = economic_activity_cell.offset(column=2).value
                        ist_value = economic_activity_cell.offset(column=3).value
                        economicActivities.append({
                            "Economic Activity": economic_activity,
                            "ACHS": achs_value,
                            "MUSEG": museg_value,
                            "IST": ist_value,
                        })
                    total_value = sum(economic_activity['ACHS'] for economic_activity in economicActivities if economic_activity['ACHS'] is not None)

                    data[category]['Total'] = total_value

                    data[category]['Economic Activities'] = economicActivities
                    
                for category, categoryInfo in data.items():
                    print(category)
                    print(f"Total: {categoryInfo['Total']}")
                    for economic_activity in categoryInfo['Economic Activities']:
                        print(f"Economic activity: {economic_activity['Economic Activity']}")
                        print(f"ACHS: {economic_activity['ACHS']}")
                        print(f"MUSEG: {economic_activity['MUSEG']}")
                        print(f"IST: {economic_activity['IST']}")
                    print()
    """
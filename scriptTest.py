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
web_page_url = "https://www.suseso.cl/608/w3-propertyvalue-10364.html"

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
                sheetsToProcess =  ['31', '29']
                for wantedSheet in sheetsToProcess:
                    if wantedSheet in workbookv2.sheetnames:
                        ws = workbookv2[wantedSheet]
                        """
                        if wantedSheet == '31':
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
                        """
                        if wantedSheet == '29':
                            print(f"switched to sheet: {ws.title}")
                            categoryData = {
                                "ACCIDENTES DEL TRABAJO": {
                                    "mutualInicio": "B8",
                                    "mutualFinal": "B11",
                                    "yearsRow": 6,
                                    "yearsColumn": ["C", "D", "E", "F", "G"],
                                },
                                "ACCIDENTES DE TRAYECTO": {
                                    "mutualInicio": "B13",
                                    "mutualFinal": "B15",
                                    "yearsRow": 6,
                                    "yearsColumn": ["C", "D", "E", "F", "G"],
                                },
                                "POR ACCIDENTES (TRABAJO + TRAYECTO)": {
                                    "mutualInicio": "B18",
                                    "mutualFinal": "B20",
                                    "yearsRow": 6,
                                    "yearsColumn": ["C", "D", "E", "F", "G"],
                                }
                            }
                            data = {}

                            for category, categoryInfo in categoryData.items():
                                data[category] = {}
                                mutualInicioCell = ws[categoryInfo["mutualInicio"]]
                                mutualFinalCell = ws[categoryInfo["mutualFinal"]]
                                yearsRow = categoryInfo["yearsRow"]
                                yearsColumn = categoryInfo["yearsColumn"]
                                
                                mutuales = []
   
                                for row in range(mutualInicioCell.row, mutualFinalCell.row + 1):
                                    mutualInicioCell = ws.cell(row=row, column=mutualInicioCell.column)
                                    mutualInicio = mutualInicioCell.value
                                    
                                    yearValues = {}
                                    percentageValues = {}

                                    for col in yearsColumn:
                                        yearValues[col] = ws[f"{col}{yearsRow}"].value 
                                        percentageValues[col] = ws[f"{col}{row}"].value
                                    
                                    mutuales.append({
                                        "Mutualidades": mutualInicio,
                                        "Year values": yearValues,
                                        "Percentage values": percentageValues
                                    })
    
                                data[category]["Mutuales"] = mutuales

                            # Print the extracted data
                            for category, categoryInfo in data.items():
                                print(f"Categoria: {category}")
                                for mutual in categoryInfo["Mutuales"]:
                                    print(f"Mutualidades: {mutual['Mutualidades']}")
                                    print(f"Year values: {mutual['Year values']}")
                                    print(f"Percentage values: {mutual['Percentage values']}")

                            """
                            categoryData = {
                                "ACCIDENTES DEL TRABAJO":{
                                    "mutualInicio": "B8",
                                    "mutualFinal": "B11",
                                    "yearsColumn": ["C", "D", "E", "F", "G"]
                                },
                                "ACCIDENTES DE TRAYECTO":{
                                    "mutualInicio": "B13",
                                    "mutualFinal": "B15",
                                    "yearsColumn": ["C", "D", "E", "F", "G"]
                                },
                                "POR ACCIDENTES (TRABAJO + TRAYECTO)":{
                                    "mutualInicio": "B18",
                                    "mutualFinal": "B20",
                                    "yearsColumn": ["C", "D", "E", "F", "G"]
                                }   
                            }
                            data = {}
                            
                            for category, categoryInfo in categoryData.items():
                                data[category] = {}
                                mutualInicioCell = ws[categoryInfo["mutualInicio"]]
                                mutualFinalCell = ws[categoryInfo["mutualFinal"]]
                                yearsColumn = categoryInfo["yearsColumn"]
                                
                                mutuales = []
                               
                                for row in range(mutualInicioCell.row, mutualFinalCell.row + 1):
                                    
                                   mutualInicio = ws.cell(row=row, column=mutualInicioCell.column).value
                                
                                   yearValues = {}
                                   for col in yearsColumn:
                                       yearValues[col] = ws[f"{col}{row}"].value
                                       
                                       mutuales.append({
                                           "Mutuales": mutualInicio,
                                           "Year values": yearValues
                                       })
                                data[category]["Mutuales"] = mutuales
                            # Print the extracted data
                            for category, categoryInfo in data.items():
                                print(f"Categoria: {category}")
                                for mutual in categoryInfo["Mutuales"]:
                                    print(f"Mutual inicio: {mutual['Mutuales']}")
                                    print(f"Year values: {mutual['Year values']}")
                        """           
                                   
                                
                                
                                
                                
                                
                                
                                
                                
                            
except requests.exceptions.RequestException as e:
        print(f"An error ocurrred while downloading the file: {e}")
        
                         
            
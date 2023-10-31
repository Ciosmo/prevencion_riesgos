# core/management/commands/custom_command.py
from django.core.management.base import BaseCommand
from core.models import EconomicActivity, Category
import requests
import pandas as pd
import os
import openpyxl
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Command(BaseCommand):
    help = 'Tu descripción de lo que hace este comando'

    def handle(self, *args, **options):
        # Tu lógica para descargar el archivo y extraer datos
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
                                        "economicActivityEnd": 'B25',
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
                                    achs_value = ws.cell(row=row, column=economicActivityStart.column + 1).value
                                    museg_value = ws.cell(row=row, column=economicActivityStart.column + 2).value
                                    ist_value = ws.cell(row=row, column=economicActivityStart.column + 3).value
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
                                
                                category_instance, created = Category.objects.get_or_create(name=category)

                                for i, economic_activity in enumerate(categoryInfo['Economic Activities']):
                                    economic_activity_instance = EconomicActivity(
                                        category=category_instance,
                                        name=economic_activity['Economic Activity'],
                                        achs=economic_activity['ACHS'],
                                        museg=economic_activity['MUSEG'],
                                        ist=economic_activity['IST'],
                                        total=total_value
                                    )
                                    economic_activity_instance.save()
                                    
        except requests.exceptions.RequestException as e:
            print(f"An error ocurrred while downloading the file: {e}")   
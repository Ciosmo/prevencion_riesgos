import requests
import os
import openpyxl
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from core.models import Category, EconomicActivity  # Importa tus modelos

web_page_url = "https://www.suseso.cl/608/w3-article-708568.html"

response = requests.get(web_page_url)

soup = BeautifulSoup(response.text, 'lxml')

downloadDir = os.path.join(os.getcwd(), "downloadedFiles")
os.makedirs(downloadDir, exist_ok=True)

try:
    for a_tag in soup.find_all('a'):
        if (
            a_tag.get("href") == "articles-708568_archivo_01.xlsx"
            and a_tag.get("title") == "Ir a Estadísticas de la Seguridad Social 2022"
        ):
            downloadUrl = "https://www.suseso.cl/608/articles-708568_archivo_01.xlsx"

            fileName = os.path.basename(downloadUrl)
            localPath = os.path.join(downloadDir, fileName)

            fileResponse = requests.get(downloadUrl)

            if fileResponse.status_code == 200:
                with open(localPath, "wb") as localFile:
                    localFile.write(fileResponse.content)
                print(f"{localPath} descargado correctamente")

                workbook = openpyxl.load_workbook(localPath)
                ws = workbook.active

                # Continúa aquí con la extracción de datos y creación de instancias de Category y EconomicActivity

                category_name = "Nombre de la categoría"  # Ajusta esto según tus datos
                category, created = Category.objects.get_or_create(name=category_name)

                # Supongamos que extraes los datos de las actividades económicas y sus valores aquí
                economic_activity_name = "Nombre de la actividad económica"
                achs_value = 123.45  # Reemplaza con el valor adecuado
                museg_value = 67.89  # Reemplaza con el valor adecuado
                ist_value = 45.67  # Reemplaza con el valor adecuado
                total_value = 234.56  # Reemplaza con el valor adecuado

                economic_activity = EconomicActivity.objects.create(
                    category=category,
                    name=economic_activity_name,
                    achs=achs_value,
                    museg=museg_value,
                    ist=ist_value,
                    total=total_value,
                )

                print("Datos almacenados en la base de datos")

except requests.exceptions.RequestException as e:
    print(f"An error occurred while downloading the file: {e}")

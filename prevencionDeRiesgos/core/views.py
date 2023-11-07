from django.shortcuts import render
from core.models import Category, EconomicActivity
import plotly.express as px
from plotly.offline import plot

# Create your views here.
def mostrar(request):
    return render(request, 'home.html')

def grafico(request):
    # Obtener los datos de tu base de datos
    datos_eco = EconomicActivity.objects.all()
    datos_category = Category.objects.all()

    # Crear un DataFrame con los datos
    import pandas as pd
    df = pd.DataFrame(list(datos_eco.values()))
    
    # Crear una nueva columna "Categoria" en el DataFrame
    def asignar_categoria(row):
        if row['category_id'] == 1:
            return 'Categoría 1'
        elif row['category_id'] == 2:
            return 'Categoría 2'
        elif row['category_id'] == 3:
            return 'Categoría 3'
        else:
            return 'Otra Categoría'
    
    df['Categoria'] = df.apply(asignar_categoria, axis=1)
    
    # Crear el gráfico utilizando Plotly Express y colorear por categoría
    fig = px.bar(df, x='name', y='achs', title='Cantidad de accidentes', color='Categoria')

    # Convierte el gráfico en HTML
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return render(request, 'home.html', {'plotly_div': plot_div})


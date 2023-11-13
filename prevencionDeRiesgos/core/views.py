from django.shortcuts import render
from core.models import Category, EconomicActivity, Mutualidad
import plotly.express as px
from plotly.offline import plot
import pandas as pd

# Create your views here.
def mostrar(request):
    return render(request, 'home.html')

def grafico(request, categoria_id=1):
    # Obtener los datos de tu base de datos
    datos_eco = EconomicActivity.objects.all()
    datos_mut = Mutualidad.objects.all()

    # Crear un DataFrame con los datos de Mutualidad
    df_mut = pd.DataFrame(list(datos_mut.values()))

    # Crear un DataFrame con los datos de EconomicActivity
    df_eco = pd.DataFrame(list(datos_eco.values()))

    def asignar_categoria(row):
        if row['category_id'] == 1:
            return 'Accidente de Trabajo'
        elif row['category_id'] == 2:
            return 'Accidente de Trayecto'
        elif row['category_id'] == 3:
            return 'Accidente de Trabajo + Trayecto'
        else:
            return 'Accidente de Trabajo + Trayecto'
    
    df_mut['Categoria'] = df_mut.apply(asignar_categoria, axis=1)
    df_eco['Categoria'] = df_eco.apply(asignar_categoria, axis=1)

    fig1 = px.bar(df_mut, x='mutual', y='anio2020', title=f'Cantidad de accidentes por Mutualidad - {categoria_id}', color='Categoria')

    fig2 = px.bar(df_eco, x='name', y='achs', title=f'Cantidad de accidentes por Actividad Económica - {categoria_id}', color='Categoria')

    # Convierte los gráficos en HTML
    plot_div1 = plot(fig1, output_type='div', include_plotlyjs=False)
    plot_div2 = plot(fig2, output_type='div', include_plotlyjs=False)

    return render(request, 'home.html', {'plotly_div1': plot_div1, 'plotly_div2': plot_div2, 'categoria_id': categoria_id})

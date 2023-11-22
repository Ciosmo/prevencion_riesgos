from core.models import EconomicActivity, Mutualidad, Tasa_Eco_Act, Sexo
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.shortcuts import redirect, render
import plotly.express as px

from plotly.offline import plot
import pandas as pd

# Create your views here.

def home(request):
    return render(request, 'home.html')

def graficoMut(request, categoria_id=1):
    # Obtener los datos de tu base de datos
    datos_eco = EconomicActivity.objects.all()
    datos_mut = Mutualidad.objects.all()
    datos_tasa_eco_act = Tasa_Eco_Act.objects.all()
    datos_sexo = Sexo.objects.all()

    # Crear un DataFrame con los datos de Mutualidad
    df_mut = pd.DataFrame(list(datos_mut.values()))

    # Crear un DataFrame con los datos de EconomicActivity
    df_eco = pd.DataFrame(list(datos_eco.values()))

    # Crear un DataFrame con los datos de EconomicActivity
    df_tasa_eco_act = pd.DataFrame(list(datos_tasa_eco_act.values()))

    # Crear un DataFrame con los datos de EconomicActivity
    df_sexo = pd.DataFrame(list(datos_sexo.values()))

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
    df_tasa_eco_act['Categoria'] = df_tasa_eco_act.apply(asignar_categoria, axis=1)
    df_sexo['Categoria'] = df_sexo.apply(asignar_categoria, axis=1)


    valores_a_eliminar = ['TOTAL ACCIDENTES DEL TRABAJO', 'TOTAL ACCIDENTES DE TRAYECTO', 'TOTAL TRABAJO Y TRAYECTO', 'TOTAL ACCIDENTES (TRABAJO + TRAYECTO)', 'TOTAL ACCIDENTES']

    # Filtrar el DataFrame para excluir las filas con los valores específicos
    df_mut = df_mut[~df_mut['mutual'].isin(valores_a_eliminar)]

    df_eco = df_eco[~df_eco['name'].isin(valores_a_eliminar)]

    df_tasa_eco_act = df_tasa_eco_act[~df_tasa_eco_act['name'].isin(valores_a_eliminar)]

    df_sexo = df_sexo[~df_sexo['name'].isin(valores_a_eliminar)]


    #Mutual

    mut1 = px.bar(df_mut, x='mutual', y='anio2018', title=f'Promedio de dias perdidos por Mutualidad segun Año', color='Categoria')

    mut2 = px.bar(df_mut, x='mutual', y='anio2019', title=f'Promedio de dias perdidos por Mutualidad segun Año', color='Categoria')

    mut3 = px.bar(df_mut, x='mutual', y='anio2020', title=f'Promedio de dias perdidos por Mutualidad segun Año', color='Categoria')

    mut4 = px.bar(df_mut, x='mutual', y='anio2021', title=f'Promedio de dias perdidos por Mutualidad segun Año', color='Categoria')

    #Actividad Economica

    eco1 = px.bar(df_eco, x='name', y='achs', title=f'Promedio de dias perdidos por Actividad Económica segun Mutualidad', color='Categoria')

    eco2 = px.bar(df_eco, x='name', y='museg', title=f'Promedio de dias perdidos por Actividad Económica segun Mutualidad', color='Categoria')

    eco3 = px.bar(df_eco, x='name', y='ist', title=f'Promedio de dias perdidos por Actividad Económica segun Mutualidad', color='Categoria')

    #Tasa 

    tea1 = px.bar(df_tasa_eco_act, x='name', y='achs', title=f'Tasa de accidentes por Actividad Económica', color='Categoria')

    tea2 = px.bar(df_tasa_eco_act, x='name', y='museg', title=f'Tasa de accidentes por Actividad Económica', color='Categoria')

    tea3 = px.bar(df_tasa_eco_act, x='name', y='ist', title=f'Tasa de accidentes por Actividad Económica', color='Categoria')

    #Sexo

    sexo1 = px.bar(df_sexo, x='name', y='men', title=f'Cantidad de accidentes por Sexo', color='Categoria')

    sexo2 = px.bar(df_sexo, x='name', y='women', title=f'Cantidad de accidentes por Sexo', color='Categoria')

    # Convierte los gráficos en HTML
    plot_div_mut1 = plot(mut1, output_type='div', include_plotlyjs=False)
    plot_div_mut2 = plot(mut2, output_type='div', include_plotlyjs=False)
    plot_div_mut3 = plot(mut3, output_type='div', include_plotlyjs=False)
    plot_div_mut4 = plot(mut4, output_type='div', include_plotlyjs=False)
    plot_div_eco1 = plot(eco1, output_type='div', include_plotlyjs=False)
    plot_div_eco2 = plot(eco2, output_type='div', include_plotlyjs=False)
    plot_div_eco3 = plot(eco3, output_type='div', include_plotlyjs=False)
    plot_div_tea1 = plot(tea1, output_type='div', include_plotlyjs=False)
    plot_div_tea2 = plot(tea2, output_type='div', include_plotlyjs=False)
    plot_div_tea3 = plot(tea3, output_type='div', include_plotlyjs=False)
    plot_div_sexo1 = plot(sexo1, output_type='div', include_plotlyjs=False)
    plot_div_sexo2 = plot(sexo2, output_type='div', include_plotlyjs=False)

    return render(request, 'Grafico.html', {'plotly_div1': plot_div_mut1,
                                            'plotly_div2': plot_div_mut2,
                                            'plotly_div3': plot_div_mut3,
                                            'plotly_div4': plot_div_mut4,
                                            'plotly_div5': plot_div_eco1,
                                            'plotly_div6': plot_div_eco2,
                                            'plotly_div7': plot_div_eco3,
                                            'plotly_div8': plot_div_tea1,
                                            'plotly_div9': plot_div_tea2,
                                            'plotly_div10': plot_div_tea3,
                                            'plotly_div11': plot_div_sexo1,
                                            'plotly_div12': plot_div_sexo2,
                                            'categoria_id': categoria_id})

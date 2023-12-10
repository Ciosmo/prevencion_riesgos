from core.models import DiasxActividad, DiasxMut, TasaxAct, AccidentesxSexo, AccidenteLaboral, EconomicActivity
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.shortcuts import redirect, render
import plotly.express as px

from plotly.offline import plot
import pandas as pd

from core.form import AccidenteForm

def home(request):
    return render(request, 'home.html')

def datosform(request):
    accidentes = AccidenteLaboral.objects.all()
    return render(request, 'GraficoForm.html', {'accidentes': accidentes})

def registrar_accidente(request):
    if request.method == 'POST':
        form = AccidenteForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('datosform')  
    else:
        form = AccidenteForm()

    return render(request, 'Formulario.html', {'form': form})

def ver_datos_relacionados(request, accidente_id):
    # Obtener el objeto AccidenteLaboral
    accidente_laboral = AccidenteLaboral.objects.get(pk=accidente_id)

    # Acceder a la actividad económica del AccidenteLaboral
    actividad_economica = accidente_laboral.actividad_economica

    # Buscar datos relacionados en la tabla DiasxActividad
    try:
        economic_activity = EconomicActivity.objects.get(activity_name=actividad_economica)
        dias_actividad = DiasxActividad.objects.get(
            category=accidente_laboral.category,
            EconomicActivity=economic_activity,
        )

        # Realizar más acciones según sea necesario...

        # Renderizar la página con los datos relacionados
        return render(request, 'ver_datos_relacionados.html', {'dias_actividad': dias_actividad})

    except EconomicActivity.DoesNotExist:
        # Manejar el caso si la actividad económica no existe
        return render(request, 'actividad_no_encontrada.html')

def grafico(request, categoria_id=1):
    # Obtener los datos de tu base de datos
    datos_eco = DiasxActividad.objects.all()
    datos_mut = DiasxMut.objects.all()
    datos_tasa_eco_act = TasaxAct.objects.all()
    datos_sexo = AccidentesxSexo.objects.all()

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
    
    df_mut['Categoria'] = df_mut.apply(lambda row: asignar_categoria(row), axis=1)
    df_eco['Categoria'] = df_eco.apply(lambda row: asignar_categoria(row), axis=1)
    df_tasa_eco_act['Categoria'] = df_tasa_eco_act.apply(lambda row: asignar_categoria(row), axis=1)
    df_sexo['Categoria'] = df_sexo.apply(lambda row: asignar_categoria(row), axis=1)

    def asignar_mutualidad(row):
        if row['mutual_id'] == 1:
            return 'Asociación Chilena de Seguridad'
        elif row['mutual_id'] == 2:
            return 'Mutual de Seguridad C.Ch.C.'
        elif row['mutual_id'] == 3:
            return 'Instituto de Seguridad del Trabajo'
        else:
            return 'Desconocida'

    df_mut['Mutualidad'] = df_mut.apply(asignar_mutualidad, axis=1)

    def asignar_actividad(row):
        if row['EconomicActivity_id'] == 1:
            return 'Agricultura, ganadería, caza y silvicultura'
        elif row['EconomicActivity_id'] == 2:
            return 'Pesca'
        elif row['EconomicActivity_id'] == 3:
            return 'Explotación de minas y canteras'
        elif row['EconomicActivity_id'] == 4:
            return 'Industrias manufactureras'
        elif row['EconomicActivity_id'] == 5:
            return 'Suministro de electricidad, gas y agua'
        elif row['EconomicActivity_id'] == 6:
            return 'Construcción'
        elif row['EconomicActivity_id'] == 7:
            return 'Comercio, reparación de vehículos y otros'
        elif row['EconomicActivity_id'] == 8:
            return 'Hoteles y restaurantes'
        elif row['EconomicActivity_id'] == 9:
            return 'Transporte, almacenamiento y comunicaciones'
        elif row['EconomicActivity_id'] == 10:
            return 'Intermediación financiera'
        elif row['EconomicActivity_id'] == 11:
            return 'Actividades inmobiliarias, empresariales y de alquiler'
        elif row['EconomicActivity_id'] == 12:
            return 'Administración publica y defensa; planes de seguridad social'
        elif row['EconomicActivity_id'] == 13:
            return 'Enseñanza'
        elif row['EconomicActivity_id'] == 14:
            return 'Servicios sociales y de salud'
        elif row['EconomicActivity_id'] == 15:
            return 'Otras actividades de servicios comunitarios, sociales y personales'
        elif row['EconomicActivity_id'] == 16:
            return 'Organizaciones y órganos extraterritoriales'
        elif row['EconomicActivity_id'] == 17:
            return 'Hogares privados con servicio doméstico'
        else:
            return 'Desconocida'
        
    df_eco['Actividad_Economica'] = df_eco.apply(asignar_actividad, axis=1)
    df_tasa_eco_act['Actividad_Economica'] = df_tasa_eco_act.apply(asignar_actividad, axis=1)
    df_sexo['Actividad_Economica'] = df_sexo.apply(asignar_actividad, axis=1)



    valores_a_eliminar = ['Desconocida']

    # Filtrar el DataFrame para excluir las filas con los valores específicos
    df_mut = df_mut[~df_mut['Mutualidad'].isin(valores_a_eliminar)]

    df_eco = df_eco[~df_eco['Actividad_Economica'].isin(valores_a_eliminar)]

    df_tasa_eco_act = df_tasa_eco_act[~df_tasa_eco_act['Actividad_Economica'].isin(valores_a_eliminar)]

    df_sexo = df_sexo[~df_sexo['Actividad_Economica'].isin(valores_a_eliminar)]


    #Mutual

    mut1 = px.bar(df_mut, x='Mutualidad', y='anio2018', title=f'Promedio de dias perdidos por Mutualidad segun Año', color='Categoria')

    mut2 = px.bar(df_mut, x='Mutualidad', y='anio2019', title=f'Promedio de dias perdidos por Mutualidad segun Año', color='Categoria')

    mut3 = px.bar(df_mut, x='Mutualidad', y='anio2020', title=f'Promedio de dias perdidos por Mutualidad segun Año', color='Categoria')

    mut4 = px.bar(df_mut, x='Mutualidad', y='anio2021', title=f'Promedio de dias perdidos por Mutualidad segun Año', color='Categoria')

    #Actividad Economica

    eco1 = px.bar(df_eco, x='Actividad_Economica', y='achs', title=f'Promedio de dias perdidos por Actividad Económica segun Mutualidad', color='Categoria')

    eco2 = px.bar(df_eco, x='Actividad_Economica', y='museg', title=f'Promedio de dias perdidos por Actividad Económica segun Mutualidad', color='Categoria')

    eco3 = px.bar(df_eco, x='Actividad_Economica', y='ist', title=f'Promedio de dias perdidos por Actividad Económica segun Mutualidad', color='Categoria')

    #Tasa 

    tea1 = px.bar(df_tasa_eco_act, x='Actividad_Economica', y='achs', title=f'Tasa de accidentes por Actividad Económica', color='Categoria')

    tea2 = px.bar(df_tasa_eco_act, x='Actividad_Economica', y='museg', title=f'Tasa de accidentes por Actividad Económica', color='Categoria')

    tea3 = px.bar(df_tasa_eco_act, x='Actividad_Economica', y='ist', title=f'Tasa de accidentes por Actividad Económica', color='Categoria')

    #Sexo

    sexo1 = px.bar(df_sexo, x='Actividad_Economica', y='men', title=f'Cantidad de accidentes por Sexo', color='Categoria')

    sexo2 = px.bar(df_sexo, x='Actividad_Economica', y='women', title=f'Cantidad de accidentes por Sexo', color='Categoria')

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

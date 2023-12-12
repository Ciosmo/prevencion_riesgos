from core.models import DiasxActividad, DiasxMut, TasaxAct, AccidentesxSexo, PorcentajexAct, FallecidosxAct, FallecidosxSexo, AccidentesxRegion, AccidenteLaboral, EconomicActivity, Region, Mutualidad
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.shortcuts import redirect, render, get_object_or_404
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
            # Obtener la instancia de EconomicActivity seleccionada
            actividad_economica = form.cleaned_data['actividad_economica']
            
            # Asignar el ID de la actividad económica al formulario antes de guardarlo
            form.instance.actividad_economica_id = actividad_economica.id
            
            # Guardar el formulario
            form.save()
            
            return redirect('datosform')  
    else:
        form = AccidenteForm()

    return render(request, 'Formulario.html', {'form': form})

def accidente_detail(request, accidente_id):

    accidente = get_object_or_404(AccidenteLaboral, pk=accidente_id)

    # Consulta otras tablas relacionadas con el AccidenteLaboral
    diasxactividad = DiasxActividad.objects.filter(EconomicActivity=accidente.actividad_economica)
    tasaxact = TasaxAct.objects.filter(EconomicActivity=accidente.actividad_economica)
    accidentesxsexo = AccidentesxSexo.objects.filter(EconomicActivity=accidente.actividad_economica)
    porcentajexact = PorcentajexAct.objects.filter(EconomicActivity=accidente.actividad_economica)
    fallecidosxact = FallecidosxAct.objects.filter(EconomicActivity=accidente.actividad_economica)
    fallecidosxsexo = FallecidosxSexo.objects.filter(EconomicActivity=accidente.actividad_economica)

    return render(request, 'accidente_detail.html', {
        'accidente': accidente,
        'diasxactividad': diasxactividad,
        'tasaxact': tasaxact,
        'accidentesxsexo': accidentesxsexo,
        'porcentajexact': porcentajexact,
        'fallecidosxact': fallecidosxact,
        'fallecidosxsexo': fallecidosxsexo
    })

def grafico(request, categoria_id=1):
    # Obtener los datos de tu base de datos
    datos_eco = DiasxActividad.objects.all()
    datos_mut = DiasxMut.objects.all()
    datos_tasa_eco_act = TasaxAct.objects.all()
    datos_sexo = AccidentesxSexo.objects.all()
    datos_deadxact = FallecidosxAct.objects.all()
    datos_deadxsexo = FallecidosxSexo.objects.all()
    datos_actxreg = AccidentesxRegion.objects.all()

    # Crear un DataFrame con los datos 
    df_mut = pd.DataFrame(list(datos_mut.values()))

    df_eco = pd.DataFrame(list(datos_eco.values()))

    df_tasa_eco_act = pd.DataFrame(list(datos_tasa_eco_act.values()))

    df_sexo = pd.DataFrame(list(datos_sexo.values()))

    df_deadxact = pd.DataFrame(list(datos_deadxact.values()))

    df_deadxsexo = pd.DataFrame(list(datos_deadxsexo.values()))

    df_actxreg = pd.DataFrame(list(datos_actxreg.values()))

    def asignar_año(row):
        if row['year_id'] == 1:
            return '2021'
        elif row['year_id'] == 2:
            return '2020'
        elif row['year_id'] == 3:
            return '2019'
        elif row['year_id'] == 4:
            return '2018'
        elif row['year_id'] == 5:
            return '2017'
        elif row['year_id'] == 6:
            return '2016'
        elif row['year_id'] == 7:
            return '2015'
        elif row['year_id'] == 8:
            return '2014'
        else:
            return ''
        
    df_mut['Año'] = df_mut.apply(lambda row: asignar_año(row), axis=1)
    df_eco['Año'] = df_eco.apply(lambda row: asignar_año(row), axis=1)
    df_tasa_eco_act['Año'] = df_tasa_eco_act.apply(lambda row: asignar_año(row), axis=1)
    df_sexo['Año'] = df_sexo.apply(lambda row: asignar_año(row), axis=1)
    df_deadxact['Año'] = df_deadxact.apply(lambda row: asignar_año(row), axis=1)
    df_deadxsexo['Año'] = df_deadxsexo.apply(lambda row: asignar_año(row), axis=1)
    df_actxreg['Año'] = df_actxreg.apply(lambda row: asignar_año(row), axis=1)

    def asignar_categoria(row):
        if row['category_id'] in [1, 5]:
            return 'Accidente de Trabajo'
        elif row['category_id'] == 2:
            return 'Accidente de Trayecto'
        elif row['category_id'] == 3:
            return 'Accidente de Trabajo + Trayecto'
        elif row['category_id'] == 6:
            return 'Enfermedades profesionales'
        else:
            return 'Desconocida'
    
    df_mut['Categoria'] = df_mut.apply(lambda row: asignar_categoria(row), axis=1)
    df_eco['Categoria'] = df_eco.apply(lambda row: asignar_categoria(row), axis=1)
    df_tasa_eco_act['Categoria'] = df_tasa_eco_act.apply(lambda row: asignar_categoria(row), axis=1)
    df_sexo['Categoria'] = df_sexo.apply(lambda row: asignar_categoria(row), axis=1)
    df_deadxact['Categoria'] = df_deadxact.apply(lambda row: asignar_categoria(row), axis=1)
    df_deadxsexo['Categoria'] = df_deadxsexo.apply(lambda row: asignar_categoria(row), axis=1)
    df_actxreg['Categoria'] = df_actxreg.apply(lambda row: asignar_categoria(row), axis=1)

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
        elif row['EconomicActivity_id'] in [4, 21]:
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
        elif row['EconomicActivity_id'] in [12, 22]:
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
    df_deadxact['Actividad_Economica'] = df_deadxact.apply(asignar_actividad, axis=1)
    df_deadxsexo['Actividad_Economica'] = df_deadxsexo.apply(asignar_actividad, axis=1)

    def asignar_region(row):
        if row['region_id'] == 1:
            return 'Arica y Parinacota'
        elif row['region_id'] == 2:
            return 'Tarapacá'
        elif row['region_id'] == 3:
            return 'Antofagasta'
        elif row['region_id'] == 4:
            return 'Atacama'
        elif row['region_id'] == 5:
            return 'Coquimbo'
        elif row['region_id'] == 6:
            return 'Valparaíso'
        elif row['region_id'] == 7:
            return 'Libertador Gral. Bdo. O*Higgins'
        elif row['region_id'] == 8:
            return 'Maule'
        elif row['region_id'] == 9:
            return 'Ñuble'
        elif row['region_id'] == 10:
            return 'Biobío'
        elif row['region_id'] == 11:
            return 'La Araucanía'
        elif row['region_id'] == 12:
            return 'Los Ríos'
        elif row['region_id'] == 13:
            return 'Los Lagos'
        elif row['region_id'] == 14:
            return 'Aysén'
        elif row['region_id'] == 15:
            return 'Magallanes y la Antártica Chilena'
        elif row['region_id'] == 16:
            return 'Metropolitana de Santiago'
        else:
            return 'Desconocida'
        
    df_actxreg['Region'] = df_actxreg.apply(asignar_region, axis=1)

    valores_a_eliminar = ['Desconocida']

    # Filtrar el DataFrame para excluir las filas con los valores específicos
    df_mut = df_mut[~df_mut['Categoria'].isin(valores_a_eliminar)]
    df_mut = df_mut[~df_mut['Mutualidad'].isin(valores_a_eliminar)]

    df_eco = df_eco[~df_eco['Categoria'].isin(valores_a_eliminar)]
    df_eco = df_eco[~df_eco['Actividad_Economica'].isin(valores_a_eliminar)]

    df_tasa_eco_act = df_tasa_eco_act[~df_tasa_eco_act['Categoria'].isin(valores_a_eliminar)]
    df_tasa_eco_act = df_tasa_eco_act[~df_tasa_eco_act['Actividad_Economica'].isin(valores_a_eliminar)]

    df_sexo = df_sexo[~df_sexo['Categoria'].isin(valores_a_eliminar)]
    df_sexo = df_sexo[~df_sexo['Actividad_Economica'].isin(valores_a_eliminar)]

    df_deadxact = df_deadxact[~df_deadxact['Categoria'].isin(valores_a_eliminar)]
    df_deadxact = df_deadxact[~df_deadxact['Actividad_Economica'].isin(valores_a_eliminar)]

    df_deadxsexo = df_deadxsexo[~df_deadxsexo['Categoria'].isin(valores_a_eliminar)]
    df_deadxsexo = df_deadxsexo[~df_deadxsexo['Actividad_Economica'].isin(valores_a_eliminar)]

    df_actxreg = df_actxreg[~df_actxreg['Categoria'].isin(valores_a_eliminar)]
    df_actxreg = df_actxreg[~df_actxreg['Region'].isin(valores_a_eliminar)]

    # Filtrar DataFrame por año
    df_eco_2021 = df_eco[df_eco['year_id'] == 1]
    df_eco_2020 = df_eco[df_eco['year_id'] == 2]
    df_eco_2019 = df_eco[df_eco['year_id'] == 3]
    df_eco_2018 = df_eco[df_eco['year_id'] == 4]
    df_eco_2017 = df_eco[df_eco['year_id'] == 5]
    df_eco_2016 = df_eco[df_eco['year_id'] == 6]
    df_eco_2015 = df_eco[df_eco['year_id'] == 7]
    df_eco_2014 = df_eco[df_eco['year_id'] == 8]

    df_deadxact_2021 = df_deadxact[df_deadxact['year_id'] == 1]
    df_deadxact_2020 = df_deadxact[df_deadxact['year_id'] == 2]
    df_deadxact_2019 = df_deadxact[df_deadxact['year_id'] == 3]
    df_deadxact_2018 = df_deadxact[df_deadxact['year_id'] == 4]
    df_deadxact_2017 = df_deadxact[df_deadxact['year_id'] == 5]
    df_deadxact_2016 = df_deadxact[df_deadxact['year_id'] == 6]
    df_deadxact_2015 = df_deadxact[df_deadxact['year_id'] == 7]
    df_deadxact_2014 = df_deadxact[df_deadxact['year_id'] == 8]

    df_actxreg_2021 = df_actxreg[df_actxreg['year_id'] == 1]
    df_actxreg_2020 = df_actxreg[df_actxreg['year_id'] == 2]
    df_actxreg_2019 = df_actxreg[df_actxreg['year_id'] == 3]
    df_actxreg_2018 = df_actxreg[df_actxreg['year_id'] == 4]
    df_actxreg_2017 = df_actxreg[df_actxreg['year_id'] == 5]
    df_actxreg_2016 = df_actxreg[df_actxreg['year_id'] == 6]
    df_actxreg_2015 = df_actxreg[df_actxreg['year_id'] == 7]
    df_actxreg_2014 = df_actxreg[df_actxreg['year_id'] == 8]

    # Crear gráficos para cada año (achs)
    eco1_2021 = px.bar(df_eco_2021, x='Actividad_Economica', y='achs', title='Promedio de días perdidos por Actividad Económica en 2021', color='Categoria')

    eco1_2020 = px.bar(df_eco_2020, x='Actividad_Economica', y='achs', title='Promedio de días perdidos por Actividad Económica en 2020', color='Categoria')

    eco1_2019 = px.bar(df_eco_2019, x='Actividad_Economica', y='achs', title='Promedio de días perdidos por Actividad Económica en 2019', color='Categoria')

    eco1_2018 = px.bar(df_eco_2018, x='Actividad_Economica', y='achs', title='Promedio de días perdidos por Actividad Económica en 2018', color='Categoria')

    eco1_2017 = px.bar(df_eco_2017, x='Actividad_Economica', y='achs', title='Promedio de días perdidos por Actividad Económica en 2017', color='Categoria')

    eco1_2016 = px.bar(df_eco_2016, x='Actividad_Economica', y='achs', title='Promedio de días perdidos por Actividad Económica en 2016', color='Categoria')

    eco1_2015 = px.bar(df_eco_2015, x='Actividad_Economica', y='achs', title='Promedio de días perdidos por Actividad Económica en 2015', color='Categoria')

    eco1_2014 = px.bar(df_eco_2014, x='Actividad_Economica', y='achs', title='Promedio de días perdidos por Actividad Económica en 2014', color='Categoria')

    #museg
    eco2_2021 = px.bar(df_eco_2021, x='Actividad_Economica', y='museg', title='Promedio de días perdidos por Actividad Económica en 2021', color='Categoria')

    eco2_2020 = px.bar(df_eco_2020, x='Actividad_Economica', y='museg', title='Promedio de días perdidos por Actividad Económica en 2020', color='Categoria')

    eco2_2019 = px.bar(df_eco_2019, x='Actividad_Economica', y='museg', title='Promedio de días perdidos por Actividad Económica en 2019', color='Categoria')

    eco2_2018 = px.bar(df_eco_2018, x='Actividad_Economica', y='museg', title='Promedio de días perdidos por Actividad Económica en 2018', color='Categoria')

    eco2_2017 = px.bar(df_eco_2017, x='Actividad_Economica', y='museg', title='Promedio de días perdidos por Actividad Económica en 2017', color='Categoria')

    eco2_2016 = px.bar(df_eco_2016, x='Actividad_Economica', y='museg', title='Promedio de días perdidos por Actividad Económica en 2016', color='Categoria')

    eco2_2015 = px.bar(df_eco_2015, x='Actividad_Economica', y='cchc', title='Promedio de días perdidos por Actividad Económica en 2015', color='Categoria')

    eco2_2014 = px.bar(df_eco_2014, x='Actividad_Economica', y='cchc', title='Promedio de días perdidos por Actividad Económica en 2014', color='Categoria')

    #ist
    eco3_2021 = px.bar(df_eco_2021, x='Actividad_Economica', y='ist', title='Promedio de días perdidos por Actividad Económica en 2021', color='Categoria')

    eco3_2020 = px.bar(df_eco_2020, x='Actividad_Economica', y='ist', title='Promedio de días perdidos por Actividad Económica en 2020', color='Categoria')

    eco3_2019 = px.bar(df_eco_2019, x='Actividad_Economica', y='ist', title='Promedio de días perdidos por Actividad Económica en 2019', color='Categoria')

    eco3_2018 = px.bar(df_eco_2018, x='Actividad_Economica', y='ist', title='Promedio de días perdidos por Actividad Económica en 2018', color='Categoria')

    eco3_2017 = px.bar(df_eco_2017, x='Actividad_Economica', y='ist', title='Promedio de días perdidos por Actividad Económica en 2017', color='Categoria')

    eco3_2016 = px.bar(df_eco_2016, x='Actividad_Economica', y='ist', title='Promedio de días perdidos por Actividad Económica en 2016', color='Categoria')

    eco3_2015 = px.bar(df_eco_2015, x='Actividad_Economica', y='ist', title='Promedio de días perdidos por Actividad Económica en 2015', color='Categoria')

    eco3_2014 = px.bar(df_eco_2014, x='Actividad_Economica', y='ist', title='Promedio de días perdidos por Actividad Económica en 2014', color='Categoria')


    # Crear gráficos para cada año (achs)
    deadxact1_2021 = px.bar(df_deadxact_2021, x='Actividad_Economica', y='achs', title='Fallecidos por Actividad Económica en 2021', color='Categoria')

    deadxact1_2020 = px.bar(df_deadxact_2020, x='Actividad_Economica', y='achs', title='Fallecidos por Actividad Económica en 2020', color='Categoria')

    deadxact1_2019 = px.bar(df_deadxact_2019, x='Actividad_Economica', y='achs', title='Fallecidos por Actividad Económica en 2019', color='Categoria')

    deadxact1_2018 = px.bar(df_deadxact_2018, x='Actividad_Economica', y='achs', title='Fallecidos por Actividad Económica en 2018', color='Categoria')

    deadxact1_2017 = px.bar(df_deadxact_2017, x='Actividad_Economica', y='achs', title='Fallecidos Actividad Económica en 2017', color='Categoria')

    deadxact1_2016 = px.bar(df_deadxact_2016, x='Actividad_Economica', y='achs', title='Fallecidos por Actividad Económica en 2016', color='Categoria')

    deadxact1_2015 = px.bar(df_deadxact_2015, x='Actividad_Economica', y='achs', title='Fallecidos por Actividad Económica en 2015', color='Categoria')

    deadxact1_2014 = px.bar(df_deadxact_2014, x='Actividad_Economica', y='achs', title='Fallecidos por Actividad Económica en 2014', color='Categoria')


    deadxact2_2021 = px.bar(df_deadxact_2021, x='Actividad_Economica', y='museg', title='Fallecidos por Actividad Económica en 2021', color='Categoria')

    deadxact2_2020 = px.bar(df_deadxact_2020, x='Actividad_Economica', y='museg', title='Fallecidos por Actividad Económica en 2020', color='Categoria')

    deadxact2_2019 = px.bar(df_deadxact_2019, x='Actividad_Economica', y='museg', title='Fallecidos por Actividad Económica en 2019', color='Categoria')

    deadxact2_2018 = px.bar(df_deadxact_2018, x='Actividad_Economica', y='museg', title='Fallecidos por Actividad Económica en 2018', color='Categoria')

    deadxact2_2017 = px.bar(df_deadxact_2017, x='Actividad_Economica', y='museg', title='Fallecidos Actividad Económica en 2017', color='Categoria')

    deadxact2_2016 = px.bar(df_deadxact_2016, x='Actividad_Economica', y='museg', title='Fallecidos por Actividad Económica en 2016', color='Categoria')

    deadxact2_2015 = px.bar(df_deadxact_2015, x='Actividad_Economica', y='cchc', title='Fallecidos por Actividad Económica en 2015', color='Categoria')

    deadxact2_2014 = px.bar(df_deadxact_2014, x='Actividad_Economica', y='cchc', title='Fallecidos por Actividad Económica en 2014', color='Categoria')


    deadxact3_2021 = px.bar(df_deadxact_2021, x='Actividad_Economica', y='ist', title='Fallecidos por Actividad Económica en 2021', color='Categoria')

    deadxact3_2020 = px.bar(df_deadxact_2020, x='Actividad_Economica', y='ist', title='Fallecidos por Actividad Económica en 2020', color='Categoria')

    deadxact3_2019 = px.bar(df_deadxact_2019, x='Actividad_Economica', y='ist', title='Fallecidos por Actividad Económica en 2019', color='Categoria')

    deadxact3_2018 = px.bar(df_deadxact_2018, x='Actividad_Economica', y='ist', title='Fallecidos por Actividad Económica en 2018', color='Categoria')

    deadxact3_2017 = px.bar(df_deadxact_2017, x='Actividad_Economica', y='ist', title='Fallecidos Actividad Económica en 2017', color='Categoria')

    deadxact3_2016 = px.bar(df_deadxact_2016, x='Actividad_Economica', y='ist', title='Fallecidos por Actividad Económica en 2016', color='Categoria')

    deadxact3_2015 = px.bar(df_deadxact_2015, x='Actividad_Economica', y='ist', title='Fallecidos por Actividad Económica en 2015', color='Categoria')

    deadxact3_2014 = px.bar(df_deadxact_2014, x='Actividad_Economica', y='ist', title='Fallecidos por Actividad Económica en 2014', color='Categoria')


    actxreg1_2021 = px.bar(df_actxreg_2021, x='Region', y='achs', title='Accidentes por Regiones en 2021', color='Categoria')

    actxreg1_2020 = px.bar(df_actxreg_2020, x='Region', y='achs', title='Accidentes por Regionesen 2020', color='Categoria')

    actxreg1_2019 = px.bar(df_actxreg_2019, x='Region', y='achs', title='Accidentes por Regiones en 2019', color='Categoria')

    actxreg1_2018 = px.bar(df_actxreg_2018, x='Region', y='achs', title='Accidentes por Regiones en 2018', color='Categoria')

    actxreg1_2017 = px.bar(df_actxreg_2017, x='Region', y='achs', title='Accidentes por Regiones en 2017', color='Categoria')

    actxreg1_2016 = px.bar(df_actxreg_2016, x='Region', y='achs', title='Accidentes por Regiones en 2016', color='Categoria')

    actxreg1_2015 = px.bar(df_actxreg_2015, x='Region', y='achs', title='Accidentes por Regiones en 2015', color='Categoria')

    actxreg1_2014 = px.bar(df_actxreg_2014, x='Region', y='achs', title='Accidentes por Regiones en 2014', color='Categoria')


    actxreg2_2021 = px.bar(df_actxreg_2021, x='Region', y='museg', title='Accidentes por Regiones en 2021', color='Categoria')

    actxreg2_2020 = px.bar(df_actxreg_2020, x='Region', y='museg', title='Accidentes por Regiones en 2020', color='Categoria')

    actxreg2_2019 = px.bar(df_actxreg_2019, x='Region', y='museg', title='Accidentes por Regiones en 2019', color='Categoria')

    actxreg2_2018 = px.bar(df_actxreg_2018, x='Region', y='museg', title='Accidentes por Regiones en 2018', color='Categoria')

    actxreg2_2017 = px.bar(df_actxreg_2017, x='Region', y='museg', title='Accidentes por Regiones en 2017', color='Categoria')

    actxreg2_2016 = px.bar(df_actxreg_2016, x='Region', y='museg', title='Accidentes por Regiones en 2016', color='Categoria')

    actxreg2_2015 = px.bar(df_actxreg_2015, x='Region', y='museg', title='Accidentes por Regiones en 2015', color='Categoria')

    actxreg2_2014 = px.bar(df_actxreg_2014, x='Region', y='museg', title='Accidentes por Regiones en 2014', color='Categoria')

    
    actxreg3_2021 = px.bar(df_actxreg_2021, x='Region', y='ist', title='Accidentes por Regiones en 2021', color='Categoria')

    actxreg3_2020 = px.bar(df_actxreg_2020, x='Region', y='ist', title='Accidentes por Regiones en 2020', color='Categoria')

    actxreg3_2019 = px.bar(df_actxreg_2019, x='Region', y='ist', title='Accidentes por Regiones en 2019', color='Categoria')

    actxreg3_2018 = px.bar(df_actxreg_2018, x='Region', y='ist', title='Accidentes por Regiones en 2018', color='Categoria')

    actxreg3_2017 = px.bar(df_actxreg_2017, x='Region', y='ist', title='Accidentes por Regiones en 2017', color='Categoria')

    actxreg3_2016 = px.bar(df_actxreg_2016, x='Region', y='ist', title='Accidentes por Regiones en 2016', color='Categoria')

    actxreg3_2015 = px.bar(df_actxreg_2015, x='Region', y='ist', title='Accidentes por Regiones en 2015', color='Categoria')

    actxreg3_2014 = px.bar(df_actxreg_2014, x='Region', y='ist', title='Accidentes por Regiones en 2014', color='Categoria')
    

    # Ejemplo con un gráfico
    mut1 = px.bar(df_mut, x='Mutualidad', y='anio2018', title=f'Promedio de días perdidos por Mutualidad según Año', color='Categoria')
    mut2 = px.bar(df_mut, x='Mutualidad', y='anio2019', title=f'Promedio de días perdidos por Mutualidad según Año', color='Categoria')
    mut3 = px.bar(df_mut, x='Mutualidad', y='anio2020', title=f'Promedio de días perdidos por Mutualidad según Año', color='Categoria')
    mut4 = px.bar(df_mut, x='Mutualidad', y='anio2021', title=f'Promedio de días perdidos por Mutualidad según Año', color='Categoria')

    # Actividad Economica
    eco1 = px.bar(df_eco, x='Actividad_Economica', y='achs', title=f'Promedio de días perdidos por Actividad Económica según Mutualidad', color='Categoria')
    eco2 = px.bar(df_eco, x='Actividad_Economica', y='museg', title=f'Promedio de días perdidos por Actividad Económica según Mutualidad', color='Categoria')
    eco3 = px.bar(df_eco, x='Actividad_Economica', y='ist', title=f'Promedio de días perdidos por Actividad Económica según Mutualidad', color='Categoria')

    # Tasa
    tea1 = px.bar(df_tasa_eco_act, x='Actividad_Economica', y='achs', title=f'Tasa de accidentes por Actividad Económica', color='Categoria')
    tea2 = px.bar(df_tasa_eco_act, x='Actividad_Economica', y='museg', title=f'Tasa de accidentes por Actividad Económica', color='Categoria')
    tea3 = px.bar(df_tasa_eco_act, x='Actividad_Economica', y='ist', title=f'Tasa de accidentes por Actividad Económica', color='Categoria')

    # Sexo
    sexo1 = px.bar(df_sexo, x='Actividad_Economica', y='men', title=f'Cantidad de accidentes por Sexo', color='Categoria')
    sexo2 = px.bar(df_sexo, x='Actividad_Economica', y='women', title=f'Cantidad de accidentes por Sexo', color='Categoria')

    #FallecidosxAct
    deadact1 = px.bar(df_eco, x='Actividad_Economica', y='achs', title=f'Fallecidos por Actividad Económica según Mutualidad', color='Categoria')
    deadact2 = px.bar(df_eco, x='Actividad_Economica', y='museg', title=f'Fallecidos por Actividad Económica según Mutualidad', color='Categoria')
    deadact3 = px.bar(df_eco, x='Actividad_Economica', y='ist', title=f'Fallecidos por Actividad Económica según Mutualidad', color='Categoria')

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
    plot_div_deadact1 = plot(deadact1, output_type='div', include_plotlyjs=False)
    plot_div_deadact2 = plot(deadact2, output_type='div', include_plotlyjs=False)
    plot_div_deadact3 = plot(deadact3, output_type='div', include_plotlyjs=False)

    plot_div_eco1_2021 = plot(eco1_2021, output_type='div', include_plotlyjs=False)
    plot_div_eco1_2020 = plot(eco1_2020, output_type='div', include_plotlyjs=False)
    plot_div_eco1_2019 = plot(eco1_2019, output_type='div', include_plotlyjs=False)
    plot_div_eco1_2018 = plot(eco1_2018, output_type='div', include_plotlyjs=False)
    plot_div_eco1_2017 = plot(eco1_2017, output_type='div', include_plotlyjs=False)
    plot_div_eco1_2016 = plot(eco1_2016, output_type='div', include_plotlyjs=False)
    plot_div_eco1_2015 = plot(eco1_2015, output_type='div', include_plotlyjs=False)
    plot_div_eco1_2014 = plot(eco1_2014, output_type='div', include_plotlyjs=False)

    plot_div_eco2_2021 = plot(eco2_2021, output_type='div', include_plotlyjs=False)
    plot_div_eco2_2020 = plot(eco2_2020, output_type='div', include_plotlyjs=False)
    plot_div_eco2_2019 = plot(eco2_2019, output_type='div', include_plotlyjs=False)
    plot_div_eco2_2018 = plot(eco2_2018, output_type='div', include_plotlyjs=False)
    plot_div_eco2_2017 = plot(eco2_2017, output_type='div', include_plotlyjs=False)
    plot_div_eco2_2016 = plot(eco2_2016, output_type='div', include_plotlyjs=False)
    plot_div_eco2_2015 = plot(eco2_2015, output_type='div', include_plotlyjs=False)
    plot_div_eco2_2014 = plot(eco2_2014, output_type='div', include_plotlyjs=False)

    plot_div_eco3_2021 = plot(eco3_2021, output_type='div', include_plotlyjs=False)
    plot_div_eco3_2020 = plot(eco3_2020, output_type='div', include_plotlyjs=False)
    plot_div_eco3_2019 = plot(eco3_2019, output_type='div', include_plotlyjs=False)
    plot_div_eco3_2018 = plot(eco3_2018, output_type='div', include_plotlyjs=False)
    plot_div_eco3_2017 = plot(eco3_2017, output_type='div', include_plotlyjs=False)
    plot_div_eco3_2016 = plot(eco3_2016, output_type='div', include_plotlyjs=False)
    plot_div_eco3_2015 = plot(eco3_2015, output_type='div', include_plotlyjs=False)
    plot_div_eco3_2014 = plot(eco3_2014, output_type='div', include_plotlyjs=False)


    plot_div_deadxact1_2021 = plot(deadxact1_2021, output_type='div', include_plotlyjs=False)
    plot_div_deadxact1_2020 = plot(deadxact1_2020, output_type='div', include_plotlyjs=False)
    plot_div_deadxact1_2019 = plot(deadxact1_2019, output_type='div', include_plotlyjs=False)
    plot_div_deadxact1_2018 = plot(deadxact1_2018, output_type='div', include_plotlyjs=False)
    plot_div_deadxact1_2017 = plot(deadxact1_2017, output_type='div', include_plotlyjs=False)
    plot_div_deadxact1_2016 = plot(deadxact1_2016, output_type='div', include_plotlyjs=False)
    plot_div_deadxact1_2015 = plot(deadxact1_2015, output_type='div', include_plotlyjs=False)
    plot_div_deadxact1_2014 = plot(deadxact1_2014, output_type='div', include_plotlyjs=False)

    plot_div_deadxact2_2021 = plot(deadxact2_2021, output_type='div', include_plotlyjs=False)
    plot_div_deadxact2_2020 = plot(deadxact2_2020, output_type='div', include_plotlyjs=False)
    plot_div_deadxact2_2019 = plot(deadxact2_2019, output_type='div', include_plotlyjs=False)
    plot_div_deadxact2_2018 = plot(deadxact2_2018, output_type='div', include_plotlyjs=False)
    plot_div_deadxact2_2017 = plot(deadxact2_2017, output_type='div', include_plotlyjs=False)
    plot_div_deadxact2_2016 = plot(deadxact2_2016, output_type='div', include_plotlyjs=False)
    plot_div_deadxact2_2015 = plot(deadxact2_2015, output_type='div', include_plotlyjs=False)
    plot_div_deadxact2_2014 = plot(deadxact2_2014, output_type='div', include_plotlyjs=False)

    plot_div_deadxact3_2021 = plot(deadxact3_2021, output_type='div', include_plotlyjs=False)
    plot_div_deadxact3_2020 = plot(deadxact3_2020, output_type='div', include_plotlyjs=False)
    plot_div_deadxact3_2019 = plot(deadxact3_2019, output_type='div', include_plotlyjs=False)
    plot_div_deadxact3_2018 = plot(deadxact3_2018, output_type='div', include_plotlyjs=False)
    plot_div_deadxact3_2017 = plot(deadxact3_2017, output_type='div', include_plotlyjs=False)
    plot_div_deadxact3_2016 = plot(deadxact3_2016, output_type='div', include_plotlyjs=False)
    plot_div_deadxact3_2015 = plot(deadxact3_2015, output_type='div', include_plotlyjs=False)
    plot_div_deadxact3_2014 = plot(deadxact3_2014, output_type='div', include_plotlyjs=False)


    plot_div_actxreg1_2021 = plot(actxreg1_2021, output_type='div', include_plotlyjs=False)
    plot_div_actxreg1_2020 = plot(actxreg1_2020, output_type='div', include_plotlyjs=False)
    plot_div_actxreg1_2019 = plot(actxreg1_2019, output_type='div', include_plotlyjs=False)
    plot_div_actxreg1_2018 = plot(actxreg1_2018, output_type='div', include_plotlyjs=False)
    plot_div_actxreg1_2017 = plot(actxreg1_2017, output_type='div', include_plotlyjs=False)
    plot_div_actxreg1_2016 = plot(actxreg1_2016, output_type='div', include_plotlyjs=False)
    plot_div_actxreg1_2015 = plot(actxreg1_2015, output_type='div', include_plotlyjs=False)
    plot_div_actxreg1_2014 = plot(actxreg1_2014, output_type='div', include_plotlyjs=False)

    plot_div_actxreg2_2021 = plot(actxreg2_2021, output_type='div', include_plotlyjs=False)
    plot_div_actxreg2_2020 = plot(actxreg2_2020, output_type='div', include_plotlyjs=False)
    plot_div_actxreg2_2019 = plot(actxreg2_2019, output_type='div', include_plotlyjs=False)
    plot_div_actxreg2_2018 = plot(actxreg2_2018, output_type='div', include_plotlyjs=False)
    plot_div_actxreg2_2017 = plot(actxreg2_2017, output_type='div', include_plotlyjs=False)
    plot_div_actxreg2_2016 = plot(actxreg2_2016, output_type='div', include_plotlyjs=False)
    plot_div_actxreg2_2015 = plot(actxreg2_2015, output_type='div', include_plotlyjs=False)
    plot_div_actxreg2_2014 = plot(actxreg2_2014, output_type='div', include_plotlyjs=False)

    plot_div_actxreg3_2021 = plot(actxreg3_2021, output_type='div', include_plotlyjs=False)
    plot_div_actxreg3_2020 = plot(actxreg3_2020, output_type='div', include_plotlyjs=False)
    plot_div_actxreg3_2019 = plot(actxreg3_2019, output_type='div', include_plotlyjs=False)
    plot_div_actxreg3_2018 = plot(actxreg3_2018, output_type='div', include_plotlyjs=False)
    plot_div_actxreg3_2017 = plot(actxreg3_2017, output_type='div', include_plotlyjs=False)
    plot_div_actxreg3_2016 = plot(actxreg3_2016, output_type='div', include_plotlyjs=False)
    plot_div_actxreg3_2015 = plot(actxreg3_2015, output_type='div', include_plotlyjs=False)
    plot_div_actxreg3_2014 = plot(actxreg3_2014, output_type='div', include_plotlyjs=False)

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
                                            'plotly_div13': plot_div_deadact1,
                                            'plotly_div14': plot_div_deadact2,
                                            'plotly_div15': plot_div_deadact3,
                                            'plotly_div17': plot_div_eco1_2021,
                                            'plotly_div18': plot_div_eco1_2020,
                                            'plotly_div19': plot_div_eco1_2019,
                                            'plotly_div20': plot_div_eco1_2018,
                                            'plotly_div21': plot_div_eco1_2017,
                                            'plotly_div22': plot_div_eco1_2016,
                                            'plotly_div23': plot_div_eco1_2015,
                                            'plotly_div24': plot_div_eco1_2014,
                                            'plotly_div25': plot_div_eco2_2021,
                                            'plotly_div26': plot_div_eco2_2020,
                                            'plotly_div27': plot_div_eco2_2019,
                                            'plotly_div28': plot_div_eco2_2018,
                                            'plotly_div29': plot_div_eco2_2017,
                                            'plotly_div30': plot_div_eco2_2016,
                                            'plotly_div31': plot_div_eco2_2015,
                                            'plotly_div32': plot_div_eco2_2014,
                                            'plotly_div33': plot_div_eco3_2021,
                                            'plotly_div34': plot_div_eco3_2020,
                                            'plotly_div35': plot_div_eco3_2019,
                                            'plotly_div36': plot_div_eco3_2018,
                                            'plotly_div37': plot_div_eco3_2017,
                                            'plotly_div38': plot_div_eco3_2016,
                                            'plotly_div39': plot_div_eco3_2015,
                                            'plotly_div40': plot_div_eco3_2014,
                                            'plotly_div41': plot_div_deadxact1_2021,
                                            'plotly_div42': plot_div_deadxact1_2020,
                                            'plotly_div43': plot_div_deadxact1_2019,
                                            'plotly_div44': plot_div_deadxact1_2018,
                                            'plotly_div45': plot_div_deadxact1_2017,
                                            'plotly_div46': plot_div_deadxact1_2016,
                                            'plotly_div47': plot_div_deadxact1_2015,
                                            'plotly_div48': plot_div_deadxact1_2014,
                                            'plotly_div49': plot_div_deadxact2_2021,
                                            'plotly_div50': plot_div_deadxact2_2020,
                                            'plotly_div51': plot_div_deadxact2_2019,
                                            'plotly_div52': plot_div_deadxact2_2018,
                                            'plotly_div53': plot_div_deadxact2_2017,
                                            'plotly_div54': plot_div_deadxact2_2016,
                                            'plotly_div55': plot_div_deadxact2_2015,
                                            'plotly_div56': plot_div_deadxact2_2014,
                                            'plotly_div57': plot_div_deadxact3_2021,
                                            'plotly_div58': plot_div_deadxact3_2020,
                                            'plotly_div59': plot_div_deadxact3_2019,
                                            'plotly_div60': plot_div_deadxact3_2018,
                                            'plotly_div61': plot_div_deadxact3_2017,
                                            'plotly_div62': plot_div_deadxact3_2016,
                                            'plotly_div63': plot_div_deadxact3_2015,
                                            'plotly_div64': plot_div_deadxact3_2014,
                                            'plotly_div65': plot_div_actxreg1_2021,
                                            'plotly_div66': plot_div_actxreg1_2020,
                                            'plotly_div67': plot_div_actxreg1_2019,
                                            'plotly_div68': plot_div_actxreg1_2018,
                                            'plotly_div69': plot_div_actxreg1_2017,
                                            'plotly_div70': plot_div_actxreg1_2016,
                                            'plotly_div71': plot_div_actxreg1_2015,
                                            'plotly_div72': plot_div_actxreg1_2014,
                                            'plotly_div73': plot_div_actxreg2_2021,
                                            'plotly_div74': plot_div_actxreg2_2020,
                                            'plotly_div75': plot_div_actxreg2_2019,
                                            'plotly_div76': plot_div_actxreg2_2018,
                                            'plotly_div77': plot_div_actxreg2_2017,
                                            'plotly_div78': plot_div_actxreg2_2016,
                                            'plotly_div79': plot_div_actxreg2_2015,
                                            'plotly_div80': plot_div_actxreg2_2014,
                                            'plotly_div81': plot_div_actxreg3_2021,
                                            'plotly_div82': plot_div_actxreg3_2020,
                                            'plotly_div83': plot_div_actxreg3_2019,
                                            'plotly_div84': plot_div_actxreg3_2018,
                                            'plotly_div85': plot_div_actxreg3_2017,
                                            'plotly_div86': plot_div_actxreg3_2016,
                                            'plotly_div87': plot_div_actxreg3_2015,
                                            'plotly_div88': plot_div_actxreg3_2014,
                                            'categoria_id': categoria_id})

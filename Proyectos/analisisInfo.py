import pandas as pd
import numpy as np




# importar Dataset
datosH = pd.read_csv('ListaH.csv')



# =====REVISION Y LIMPIEZA DE DATOS====
print(datosH.info())

# cambion nombre columnas
# print(datosH.columns)					#capitalizar texto y corregir nombre
# revision datos columnas Idea general
#print(datosH['tipo'].unique())			#parece bien
# print(datosH['genero'].unique())		#separar los generos de forma individual generando nuevos registro 
# print(datosH['studios'].unique())		#revisar los null o nan 
# print(datosH['idiomas'].unique())		#parece bien de pronto elimanar acento
# print(datosH['episodios'].unique())	#cambiar a variable numerica y convertir desconocido en null
# print(datosH['duracion'].unique())	#revisar foromato tiempo, desconocido en null
# print(datosH['emitido'].unique())		#limpiar fechas formato util
# print(datosH['estado'].unique()) 		#revisar etiquetas
# print(datosH['gustados'].unique())	#parece bien 
# print(datosH['nombre'].unique())		#revisar formato



# revision de los null
print(datosH.isna().sum())



# arreglar nombre de las columnas
datosH.rename(columns = {'studios':'estudios'}, inplace = True)
datosH.columns = datosH.columns.str.capitalize()
print(datosH.columns)



# revisar las columnas con nan
# columna duracion
# remplazamos desconocido por None
datosH['Duracion'].fillna(0, inplace = True)
datosH.loc[datosH['Duracion'] == 'Desconocido', 'Duracion'] = 0

# limpiar datos formato minutos y convercion a variable numerica
datosH['Duracion'] = datosH['Duracion'].astype(str).str.replace(r'\D*','', regex = True)
datosH['Duracion'] = pd.to_numeric(datosH['Duracion'])
print(datosH.dtypes)


# columna Emitido
# limpiar y arregra en formato fecha

# Usar str.extract() con una expresión regular adecuada
datosH[['Inicio_Emision', 'Fin_Emision']] = datosH['Emitido'].str.extract(r'([A-Za-z]+\d{1,2}de\d{4})a([A-Za-z]+\d{1,2}de\d{4})')
# removemos 'de' de los registros
datosH[['Inicio_Emision', 'Fin_Emision']] = datosH[['Inicio_Emision', 'Fin_Emision']].apply(lambda x : x.str.replace('de','-').str.replace('Dic','Dec').str.replace('Abr','Apr').str.replace('Ene','Jan') )
# rellenamos los valores nulos con los valores faltantes de la coluumna Emitido
datosH['Inicio_Emision'].fillna(datosH['Emitido'].str.replace('de','-').str.replace('Dic','Dec'), inplace = True)

# print(datosH[datosH['Fin_Emision'].apply(lambda x: 'Jan' in str(x))])
# convertimos la fehas en formato fecha
datosH['Inicio_Emision'] = pd.to_datetime(datosH['Inicio_Emision'], format='%b%d-%Y', errors='coerce')
datosH['Fin_Emision'] = pd.to_datetime(datosH['Fin_Emision'], format='%b%d-%Y', errors='coerce')

print(datosH[['Emitido','Inicio_Emision','Fin_Emision']])



# limpieza formato Nombre
datosH['Nombre'] = datosH['Nombre'].astype(str).str.capitalize().str.replace('-',' ')
print(datosH['Nombre'])


# Columna Generos
# sepárammos los generos de forma individual replicando los registros de forma individual
datosH['Genero'] = datosH['Genero'].str.split(',') 	#lo primero que debemos hacer es separarlos en listas
datosH = datosH.explode('Genero').reset_index()		#y luego usamos el xzplote para que se creeen nuevos regidtors

# capitalizamos los registros de los Generos
datosH['Genero'] = datosH['Genero'].str.capitalize()  


# eliminamos columna Emitido
datosH.drop(columns = ['Emitido'], inplace = True)


# incertar nuevo registro
nuevoRegistro = datosH.loc[datosH['Nombre'].str.startswith('Shounen ga otona') ==  True].head(1).copy()
nuevoRegistro['Genero'] = 'Lolis' 
datosH = pd.concat([datosH, nuevoRegistro], ignore_index = True)
print(datosH.loc[(datosH['Nombre'] ==  'Shounen ga otona ni natta natsu') & (datosH['Genero'] ==  'Lolis')])

# revision
print(datosH.loc[:,['Genero','Nombre']].tail(2))



# =====VISUALIZACION DE DATOS======
import matplotlib.pyplot as plt



print('\n\n =====ANALISIS DE DATOS====')

# ### 1. **Análisis Descriptivo Básico:**
# - **Distribución de los tipos de programas**: Puedes analizar cuántos programas pertenecen a cada tipo (columna "Tipo").
print(datosH.groupby('Genero')['Nombre'].count().sort_values(ascending = False))
# - **Distribución por género**: Similar al análisis anterior, pero esta vez por el género (columna "Genero"). Puedes analizar qué géneros son más populares o predominantes.
print(datosH.groupby('Genero')['Gustados'].sum().sort_values(ascending = False))
# - **Duración promedio**: Calcular la duración promedio de los programas. Esto puede ser útil para comparar la longitud de los programas y ver si hay tendencias significativas según el "Tipo" o el "Genero".
print(datosH.groupby('Genero')['Duracion'].sum().sort_values(ascending = False))
print('Duracion Promedio: ',int(datosH['Duracion'].mean()))
#  - **Promedio de "Gustados"**: Ver cuál es el promedio de la columna "Gustados". Esto puede dar una idea de qué tan populares son los programas en términos de interacciones o preferencias.
print('Gustados Promedio: ', datosH['Gustados'].mean().astype(int)) 


print("numero de H's: ",len(datosH['Nombre'].unique()))
print(datosH.columns)

#### 2. **Análisis Temporal:**
# - **Distribución de los programas por fecha de emisión**: Usando las columnas de "Inicio_Emision" y "Fin_Emision", puedes ver en qué periodos del año se emiten más programas. 
# primero creamos nueva variable eliminando los duuplicados
no_Dupli_datosH = datosH.drop_duplicates(subset = ['Nombre']).copy()

# Inicio_Emision
# no_Dupli_datosH.groupby(no_Dupli_datosH['Inicio_Emision'].dt.year)['Nombre'].count().plot(kind = 'bar')
# plt.xlabel("Año")
# plt.ylabel("Cantidad de Programas x Año")
# plt.title("Programas que Iniciaron y Terminaron por Año")
# plt.legend()
# plt.grid(axis='y', linestyle="--", alpha=0.5)
# plt.show()

# fin_Emision
# no_Dupli_datosH.groupby(no_Dupli_datosH['Fin_Emision'].dt.year)['Nombre'].count().plot(kind = 'bar')
# plt.xlabel("Año")
# plt.ylabel("Cantidad de Programas x Año")
# plt.title("Programas que Finalizaron el año")
# plt.legend()
# plt.grid(axis='y', linestyle="--", alpha=0.5)
# plt.show()

# - Analizar la cantidad de programas que comenzaron o terminaron en determinados meses o años puede darte una visión sobre la estacionalidad de los programas.
# Inicio_Emision
# no_Dupli_datosH.groupby(no_Dupli_datosH['Inicio_Emision'].dt.month)['Nombre'].count().plot(kind = 'bar')
# plt.xlabel('mes')
# plt.ylabel('numero de Programas')
# plt.title('programas Iniciados x mes')
# plt.grid(axis = 'y', linestyle="--")
# # plt.show()

# Fin_Emision
# no_Dupli_datosH.groupby(no_Dupli_datosH['Fin_Emision'].dt.month)['Nombre'].count().plot(kind = 'bar')
# plt.xlabel('mes')
# plt.ylabel('numero de Programas')
# plt.title('programas Finalizados x mes')
# plt.grid(axis = 'y', linestyle="--")
# plt.show()



# Duracion promedio de cada programa
no_Dupli_datosH['Fecha_Duracion'] = no_Dupli_datosH.apply(lambda x : 0  if pd.isna(x['Fin_Emision']) else (x['Fin_Emision']- x['Inicio_Emision']).days , axis=1)
no_Dupli_datosH = no_Dupli_datosH.reset_index()

print('promedio de duracion de un anime en dias: ', no_Dupli_datosH['Fecha_Duracion'].mean().astype(int) , 'dias')


# - **Programas en emisión actualmente**: Los programas que tienen la fecha de "Fin_Emision" en null o sin una fecha de término pueden ser considerados como programas que aún están activos.

print(no_Dupli_datosH['Fin_Emision'].isna().value_counts())
# no_Dupli_datosH['Fin_Emision'].isna().value_counts().plot( kind = 'bar', color=['red', 'green'])
# plt.xlabel('No Terminado y Terminados')
# plt.ylabel('Numero de datos')
# plt.xticks(ticks=[0, 1], labels=['No Terminado', 'Terminado'], rotation=0)
# plt.grid(axis = 'y', linestyle="--")
# plt.legend().remove()
# plt.show()



# ### 3. **Análisis de Ausencias de Datos:**
#    - **Fecha de fin de emisión**: Observando que muchos programas tienen fechas de finalización nulas, podrías analizar si esos programas están más relacionados con ciertos tipos o géneros, o si corresponden a programas más nuevos.
result = no_Dupli_datosH.dropna(subset=['Fin_Emision']) \
                         .groupby('Genero')['Fin_Emision'] \
                         .count()

# result.plot( kind = 'bar')
# plt.show()


# ### 4. **Análisis de Correlación:**
#    - **Correlación entre duración y "Gustados"**: Podrías examinar si existe alguna relación entre la duración de los programas y la cantidad de "Gustados". Tal vez los programas más largos reciban más "Gustados", o puede que sea lo contrario.

print(no_Dupli_datosH.groupby('Tipo')['Genero'].count())
# no_Dupli_datosH.groupby('Tipo')['Gustados'].count().plot(kind = 'bar', color = ['green', 'red', 'blue'])
# plt.xlabel('tipo OVA, ONA o Serie')
# plt.ylabel('Gustados')
# plt.show()




# ===========IMPORTANTE EL USO DE CROSSBAR PARA VISUALIZAR LOS DATOS DIFERENTES
#    - **Correlación entre "Tipo" y "Genero"**: Es probable que los géneros varíen según el tipo de programa. ¿Por ejemplo, ciertos tipos de programas como "documentales" o "noticias" tienen un género más especializado que otros?
tabla = pd.crosstab(datosH['Genero'], datosH['Tipo'])
print(tabla)

# Genero  Accion  Ahegao  Anal  Aventura  ...  Violacion  Virgenes  Yaoi  Yuri
# Tipo                                    ...                                 
# ONA          0       3     8         0  ...         10        17     3     4
# OVA          4      44    72         1  ...        108       127     6    28
# Serie        0       0     1         0  ...          0         1     0     0


# tabla.plot(kind='bar', stacked=True, figsize=(12, 6))
# plt.show()



# ### 5. **Análisis de Programas Actuales y Terminados:**
#    - **Estado de los programas**: Usando la columna "Estado" (que tiene valores como "En emisión", "Terminada", etc.), puedes ver cuántos programas están en emisión, cuántos han finalizado y cuántos están en algún otro estado. Esto puede ser útil para analizar la dinámica de producción y cancelación de programas.

print(no_Dupli_datosH['Estado'].value_counts())



# Mejores H segun el año
no_Dupli_datosH['Año'] = no_Dupli_datosH['Inicio_Emision'].dt.year
top10_por_año = (no_Dupli_datosH.sort_values(['Año', 'Gustados'], ascending = [True, False]).groupby('Año').head(1)) # podés cambiar a 3 o 5 si querés más de uno por año
print(top10_por_año[['Año', 'Nombre', 'Gustados']])


# Usando pivot 
pivot = top10_por_año.pivot_table(
    index='Año',
    columns='Nombre',
    values='Gustados',
    aggfunc='sum'
).fillna(0)

print(pivot)
# Nombre  Bible black  ...  Yuuwaku countdown
# Año                  ...                   
# 1995.0          0.0  ...                4.0


# grafica
pivot.plot(
    kind='bar',
    stacked=True,
    figsize=(14, 8),
    colormap='tab20'
)

plt.show()




# GUARDADO DE DATASETS
# datosH.to_csv('NuevaListaH.csv', index = False)
# no_Dupli_datosH.to_csv('NoDupNuevaListaH.csv', index = False)

















#!/usr/bin/env python
# coding: utf-8

# En este ejer ejercicio realizaremos una clasificación de colonias por el tipo de caracteristicas de la vivienda, sirviendo como un proxy de nivel socio económico de la ciudad de México. <br>
# To esto, usando datos del Censo de Población y Vivienda 2020.

# In[2]:


# Importamos librerías a ocupar

# Ajusta el tamalo de los graficos al de la ventana
get_ipython().run_line_magic('matplotlib', 'inline')

import requests
# Visualiza tiempo de ejercución de procesos
from tqdm import tqdm
#
from zipfile import ZipFile 
#
import time
#
import os
#
import shutil
# Visualización de datos
import seaborn as sns
# Trabajo de bases de datos
import pandas as pd
# Trabajo de información tabular geografíca
import geopandas as gpd

# Analisis espacial
from pysal.lib import weights
# Datos de ejemplo de pysal
from pysal.lib import examples
# Mapas base
import contextily as cx
# Cosas matemáticas
import numpy as np
# Visualización de datos
import matplotlib.pyplot as plt
# Machine Learning
from sklearn import cluster
# Algoritmo kmeans
from sklearn.cluster import KMeans
# Algoritmo kmeans
from sklearn_extra.cluster import KMedoids
# Calculo de distancia entre puntos
from scipy.spatial.distance import cdist


# # Descarga de la información
# La primera parte de este tutorial se basa en el trabajo de Abel Coronado, con el cual se puede descargar información del censo 2020 e integrarla con su respectiva geometria

# In[4]:


#Función para descargar información
def download(url,dir):
    time.sleep(5)
    chunk_size = 1024
    r = requests.get(url, stream = True)
    total_size = int(r.headers['content-length'])
    filename = url.split('/')[-1]
    with open(dir+filename, 'wb') as f:
        for data in tqdm(iterable = r.iter_content(chunk_size = chunk_size), total = total_size/chunk_size, unit = 'KB'):
            f.write(data)


# In[5]:


# Definimos la pagina de la que se descargara la información
ageb_mza = f'https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_09_cpv2020_csv.zip'
# Definimos el lugar donde se descargara la información
directory= "./Datos/"
# Aplicamos la función download, dando como parametros la dirección de descarga y el directorio en el que guardar los datos
download(ageb_mza,directory)


# In[6]:


# Establecemos el directorio en donde se guardara la información descargada
directory= "./Datos/"
# Definimos la pagina de la que se descargara la información
url_mgccpv = "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/889463807469/09_ciudaddemexico.zip"
# Aplicamos la función download, dando como parametros la dirección de descarga y el directorio en el que guardar los datos
download(url_mgccpv,directory)


# In[7]:


# Extracción de datos del censo 2020
# Definimos directorio donde se encuentra la información
directory= "./Datos/"
# Indicamos la ruta donde se encuentra archivo comprimido
zip_file = directory+f'ageb_mza_urbana_09_cpv2020_csv.zip'
# Ruta donde se guardara el archivo csv extraido
csv_file = f'conjunto_de_datos/conjunto_de_datos_ageb_urbana_09_cpv2020.csv'
# Extraemos los archivos
with ZipFile(zip_file, 'r') as zip:
    zip.extract(csv_file,directory)


# In[8]:


# Extraemos los shapefiles
# Seleccionamos el tipo de informacióna  descargar a = ageb
shape_type = "a"
directory= "./Datos/"
shp_dir = "./Datos/"
# archivo_zip = ['09_ciudaddemexico.zip']
states = ["09_ciudaddemexico.zip"]

# Ciclo para extraer los archivos que componen al shp
for i in range(1):
    estado = states[i]
    # el número real debería ser i+1
    file = str(i+9).zfill(2)
    zip_file = directory+estado
    shp_file = f'conjunto_de_datos/{file}{shape_type}.shp'
    cpg_file = f'conjunto_de_datos/{file}{shape_type}.cpg'
    dbf_file = f'conjunto_de_datos/{file}{shape_type}.dbf'
    prj_file = f'conjunto_de_datos/{file}{shape_type}.prj'
    shx_file = f'conjunto_de_datos/{file}{shape_type}.shx'
    with ZipFile(zip_file, 'r') as zip:
        zip.extract(shp_file,shp_dir)
        zip.extract(dbf_file,shp_dir)
        zip.extract(prj_file,shp_dir)
        zip.extract(shx_file,shp_dir)
        try:
            zip.extract(cpg_file,shp_dir)
        except:
            with open(shp_dir+cpg_file, 'w') as out_file:
                out_file.write("ISO 88591")

#extract_shapefile(states,directory,shp_dir,shape_type)

# ./Datos/ + 09_ciudaddemexico.zip = extrae shapes
# ./Datos/ + 


# In[9]:


# Lectura de shp de agebs
gpdf = gpd.read_file(f"./Datos/conjunto_de_datos/09a.shp")
# Visualizamos
gpdf.head()


# In[10]:


# Lectura de csv, y definiendo valores nulos
df = pd.read_csv(f"./Datos/conjunto_de_datos/conjunto_de_datos_ageb_urbana_09_cpv2020.csv",na_values=['N/A','N/D','*'])
# Visualizamos
df.head()


# In[11]:


# Creación de columna geoclave, apartir de las columnas ENTIDAD, MUN, LOC,  y AGEB
# df['CVEGEO'] = df.apply(lambda row: str(row['ENTIDAD']).zfill(2) + str(row['MUN']).zfill(3)+ str(row['LOC']).zfill(4)+ str(row['AGEB']).zfill(4)+ str(row['MZA']).zfill(3), axis=1)
df['CVEGEO'] = df.apply(lambda row: str(row['ENTIDAD']).zfill(2) + str(row['MUN']).zfill(3)+ str(row['LOC']).zfill(4)+ str(row['AGEB']).zfill(4), axis=1)

# Unión entre geometria e información tabular
df_geo_censo = pd.merge(df, gpdf, how = 'left').drop(["CVE_ENT", "CVE_MUN", "CVE_LOC", "CVE_AGEB"], axis = 1)

# Removemos todo aquello que no sean manzanas, es decir, donde el valor de la columna MZA = 0
df_geo_censo = df_geo_censo.drop(df[df.NOM_LOC != 'Total AGEB urbana'].index)

# Convertimos a geodataframe
df_geo_censo = gpd.GeoDataFrame(df_geo_censo, geometry="geometry")

# Reproyectamos a su zona UTM
df_geo_censo = df_geo_censo.to_crs("EPSG:32614")


# In[12]:


# Ya que se termino la descarga procedemos a eliminar los archivos descargados
directory = "./Datos/"
# Ciclo para remover archivos y carpertas dentro del directorio
for root, dirs, files in os.walk(directory):
    for file in files:
        os.remove(os.path.join(root, file))
        print("Archivos borrados")


# In[13]:


df_geo_censo.head()


# # Preprocesamiento de la información

# In[14]:


# Variable que contiene los encabezados de las columnas de interes
filtro = ['geometry','CVEGEO','GRAPROES','PRO_OCUP_C','TVIVPARHAB','VPH_PISOTI', 'VPH_3YMASC','VPH_TINACO','VPH_CISTER','VPH_REFRI','VPH_LAVAD','VPH_HMICRO','VPH_AUTOM','VPH_MOTO','VPH_TV','VPH_PC','VPH_TELEF','VPH_CEL','VPH_INTER','VPH_STVP','VPH_SPMVPI','VPH_CVJ']


# In[15]:


# creamos nueevo gdf apartir del filtro
gdf = df_geo_censo[filtro]
# Visualizamos caracteristicas generales
gdf.info()


# In[16]:


# Contamos el número de valores nulos en cada columna
print(" \nConteo de valores nulos en el dataframe : \n\n", 
      gdf.isnull().sum()) 


# In[17]:


# Filtramos solo aquellas manzanas que sean poligonos
gdf = gdf[gdf.geometry.type == 'Polygon']
# Removelos valores nulos en la columna de total de viviendas particulares habitadas
gdf = gdf.dropna(subset=['TVIVPARHAB'])


# In[18]:


# Remplazamos todos los demás valores en las columnas con 0
gdf = gdf.fillna(0)
# Contamos los nulos
print(" \nConteo de valores nulos en el dataframe : \n\n", 
      gdf.isnull().sum()) 


# In[17]:


# Obtenemos el centroide de los poligonos para unirla al archivo de colonias
# gdf['geometry'] = gdf.centroid
#
# gdf.head()


# # Agregación -  De manzanas a colonias

# In[23]:


# Cargamos la capa de colonias de la ciudad de México
# el archivo original puede ser descargado en https://datos.cdmx.gob.mx/dataset/04a1900a-0c2f-41ed-94dc-3d2d5bad4065/resource/03368e1e-f05e-4bea-ac17-58fc650f6fee/download/coloniascdmx.csv
#col = gpd.read_file('E:/aloac/Documents/Datos/Colonias_CDMX/colonias_cdmx.geojson')
#col.head()


# In[24]:


# Filtramos columnas de interes
#col = col.filter(['id', 'nombre', 'alcaldia','cve_col','geometry',])
# Visualizamos
#col.head()


# In[25]:


# Se procede a realizar el join espacial, en la que cada entidad de la capa de manzanas, obtendra la clave de colonia en la que se encuentra
#gdf = gpd.sjoin(gdf, col, how="inner", op="intersects")
#gdf.head()


# In[26]:


#gdf_mean = gdf.groupby(['cve_col'],as_index=False)['PRO_OCUP_C'].mean()
#gdf_mean.head()


# In[27]:


# Caracteristicas de la vivienda sumar
#carac =  ['TVIVPARHAB','VPH_PISOTI','VPH_3YMASC','VPH_TINACO','VPH_CISTER','VPH_REFRI','VPH_LAVAD','VPH_HMICRO','VPH_AUTOM','VPH_MOTO','VPH_TV','VPH_PC','VPH_TELEF','VPH_CEL','VPH_INTER','VPH_STVP','VPH_SPMVPI','VPH_CVJ']
# Aregación de lod datos por clave de colonia
#gdf_sum = gdf.groupby(['cve_col'],as_index=False)[carac].sum()
# Visualización
#gdf_sum.head()


# In[28]:


# Unión entre los dos dataframes
#gdf = pd.merge(gdf_mean, gdf_sum, how = 'left')
#gdf.head()


# In[29]:


# # Unión entre geometria e información tabular
#gdf = pd.merge(gdf, col, how = 'left')
#gdf.head()


# # Calculo de porcentajes

# In[19]:


# Definimos las columnas de las cuales obtendremos los porcentajes
carac =  ['VPH_PISOTI', 'VPH_3YMASC','VPH_TINACO','VPH_CISTER','VPH_REFRI','VPH_LAVAD','VPH_HMICRO','VPH_AUTOM','VPH_MOTO','VPH_TV','VPH_PC','VPH_TELEF','VPH_CEL','VPH_INTER','VPH_STVP','VPH_SPMVPI','VPH_CVJ']
# Se crea una variable que tendrá los porcentajes para cada etnia
pcts = gdf[carac].divide(gdf["TVIVPARHAB"], axis=0)
# Join entre tabla de etnias y tabla base
gdf = gdf.join(pcts, rsuffix="_pct")
# Visualizamos
gdf.head()


# In[20]:


gdf.info()


# In[21]:


# Creamos una variable que contenga solo los valores de porcentaje
housing_pcts = [i + "_pct" for i in carac]
#
housing_pcts.append('PRO_OCUP_C')
housing_pcts.append('GRAPROES')
#
gdf[housing_pcts].info()


# In[22]:


# Remplazamos todos los demás valores en las columnas con 0
gdf = gdf.fillna(0)
# Contamos los nulos
print(" \nConteo de valores nulos en el dataframe : \n\n", 
      gdf.isnull().sum()) 


# In[23]:


# Removemos las filas con valores nulos y creamos una variable que contenga estos datos
gdf_cluster = gdf[housing_pcts + ["geometry"]]
gdf_cluster.head()


# In[24]:


gdf_codo = gdf[housing_pcts].dropna()
gdf_codo.head()


# In[25]:


gdf_codo.describe()


# In[32]:


# Create figure and axes (this time it's 9, arranged 3 by 3)
f, axs = plt.subplots(nrows=3, ncols=7, figsize=(35, 20))
# Make the axes accessible with single indexing
axs = axs.flatten()
# Start the loop over all the variables of interest
for i, col in enumerate(housing_pcts):
    # select the axis where the map will go
    ax = axs[i]
    # Plot the map
    gdf.plot(column=col, ax=ax, scheme='Quantiles',              linewidth=0, cmap='viridis', alpha=0.75)
    # Remove axis clutter
    ax.set_axis_off()
    # Set the axis title to the name of variable being plotted
    ax.set_title(col)
# Display the figure
plt.show()


# In[27]:


#Using Pearson Correlation
plt.figure(figsize=(20,20))
cor = gdf[housing_pcts].corr()
sns.heatmap(cor, annot=True, cmap='RdYlGn')
plt.show()


# In[28]:


#Correlation with output variable
cor_target = abs(cor["GRAPROES"])
#Selecting highly correlated features
relevant_features = cor_target[cor_target<0.45]
relevant_features


# In[33]:


# Removemos columnas que no son de interes
gdf_codo = gdf_codo.drop(columns=['VPH_PISOTI_pct','VPH_MOTO_pct','VPH_TINACO_pct', 'VPH_TINACO_pct', 'VPH_TV_pct'])
# Visualizamos
gdf_codo.head()


# In[34]:


# Recreamos la variable housing_pcts a partir del nombre de columnas de gdf_codo
housing_pcts = gdf_codo.columns.tolist()
housing_pcts


# In[35]:


gdf_cluster = gdf[ ["CVEGEO"] + ["geometry"] + housing_pcts]
gdf_cluster.head()


# In[ ]:





# # Estimar el número de Cluster

# In[30]:


from yellowbrick.cluster import KElbowVisualizer


# In[31]:


# Inicializamos el modelo y el visualizador
# Instantiate the clustering model and visualizer
model = KMeans()
visualizer = KElbowVisualizer(model, k=(2,12))
# Ajustamos los datos al modelo
visualizer.fit(gdf_codo)
# Visualizamos la grafica
visualizer.show()        # Finalize and render the figure


# # K-Means

# In[32]:


#Establecemos el número de clusters = 3
kmeans5 = cluster.KMeans(n_clusters=5, random_state=12345)
# Corremos kmeans
k5cls = kmeans5.fit(gdf_cluster[housing_pcts])
#Agregamos etiquetas a la base 
gdf_cluster['k5cls'] = k5cls.labels_


# In[33]:



# Setup figure and ax
f, ax = plt.subplots(1, figsize=(18, 18))
# Plot underlying geometries of all areas 
#in light grey and white borders
gdf.plot(ax=ax, 
         facecolor="grey", 
         edgecolor="w", 
         alpha=0.5
        )
# Plot unique values choropleth including 
#a legend and with no boundary lines
gdf_cluster.plot(column='k5cls', 
                    categorical=True, 
                    cmap="viridis",
                    legend=True, 
                    linewidth=0, 
                    ax=ax
                   )
# Remove axis
ax.set_axis_off()
# Add title
plt.title('Segmentación geodemográfica de la vivienda en la Ciudad de México')
# Display the map
plt.show()


# In[54]:


# gdf_cluster['k5cls'] = k5cls.labels_
gdf['k5cls'] = k5cls.labels_
gdf.head()


# In[65]:


# Calcular el promedio de proporción de población por etnia
k5means = gdf_cluster.groupby('k5cls')[housing_pcts].mean()
k5means.index.name = "Clusters"
k5means.columns.name = "Variables"
# Show the table transposed (so it's not too wide)
k5means.T


# In[67]:


k5means['total'] = k5means.sum(axis=1)
k5means.sort_values(by=['total'], ascending=False)


# In[35]:


# Caracteristicas de los clusters
# Número de entidades por cluster
k5sizes = gdf_cluster.groupby('k5cls').size()
k5sizes


# # k-Medoids

# In[37]:


#Establecemos el número de clusters = 3
kmedoid5 = KMedoids(n_clusters=5, random_state=12345)
# Corremos kmeans
kmedoid5cls = kmedoid5.fit(gdf_cluster[housing_pcts])
#Agregamos etiquetas a la base 
gdf_cluster['kmdoid5cls'] = kmedoid5cls.labels_


# In[38]:


# Setup figure and ax
f, ax = plt.subplots(1, figsize=(18, 18))
# Plot underlying geometries of all areas 
#in light grey and white borders
gdf.plot(ax=ax, 
         facecolor="grey", 
         edgecolor="w", 
         alpha=0.5
        )
# Plot unique values choropleth including 
#a legend and with no boundary lines
gdf_cluster.plot(column='kmdoid5cls', 
                    categorical=True, 
                    cmap="viridis",
                    legend=True, 
                    linewidth=0, 
                    ax=ax
                   )
# Remove axis
ax.set_axis_off()
# Add title
plt.title('Segmentación geodemográfica de la vivienda en la Ciudad de México')
# Display the map
plt.show()


# In[39]:


# Calcular el promedio de proporción de población por etnia
k5medoids = gdf_cluster.groupby('kmdoid5cls')[housing_pcts].mean()
k5medoids.index.name = "Clusters"
k5medoids.columns.name = "Variables"
# Show the table transposed (so it's not too wide)
k5medoids.T


# # Regionalización

# In[37]:


w = weights.Queen.from_dataframe(gdf)


# In[38]:


reg5 = cluster.AgglomerativeClustering(n_clusters=5, connectivity=w.sparse)
reg5


# In[39]:


# Run the clustering algorithm
reg5cls = reg5.fit(gdf[housing_pcts])


# In[49]:


reg5cls.labels_


# In[53]:


ax = gdf.assign(labels=reg5cls.labels_)                  .dissolve("labels")                  .reset_index()                  .plot(legend=True, 
                  column="labels",
                        edgecolor="black",
                        alpha=0.75,
                        categorical=True,
                        figsize=(18, 18)
                       )
cx.add_basemap(ax,crs=gdf.crs,source=cx.providers.Esri.WorldImagery)


# In[51]:


gdf['reg5cls'] = reg5cls.labels_
gdf.head()


# In[52]:


# Calcular el promedio de proporción de población por etnia
regg5 = gdf.groupby('reg5cls')[housing_pcts].mean()
regg5.index.name = "Clusters"
regg5.columns.name = "Variables"
# Show the table transposed (so it's not too wide)
regg5.T


# In[68]:


regg5['total'] = regg5.sum(axis=1)
regg5.sort_values(by=['total'], ascending=False)


# In[55]:


gdf.to_file("E:/aloac/Documents/Notebooks/00_Archivos resultado/clustering_cdmx_nseproxy.geojson", driver='GeoJSON')


# In[ ]:





# In[ ]:





# In[ ]:





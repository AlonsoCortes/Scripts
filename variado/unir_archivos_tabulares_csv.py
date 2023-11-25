import pandas as pd
import os
import glob
warnings.filterwarnings('ignore')

'''
Este archivo presenta la función para agrupar en un solo archivo distintos archivos tabulares csv
'''

def agrupar_csv(ruta, nombre_salida):
    
 """
    Genera un procesamiento para agrupar en un solo archivo distintos archivos tabulares csv.

    Parámetros
    ----------
    ruta : str
        Ruta de los archivos csv a agrupar.
    nombre_salida : str
        Nombre de salida del archivo agrupado.

    Regresa
    -------
    CSV
        Un csv con los csv agrupados.
    """
    
    archivos = glob.glob(os.path.join(ruta, "*.csv"))
    lista = []
    for archivo in archivos:
        df = df = pd.read_csv(archivo, index_col=None, header=0)
        df['archivo'] = archivo
        lista.append(df)
        
    df = pd.concat(lista, axis=0, ignore_index=True)
    df.to_csv(f"{nombre_salida}.csv")
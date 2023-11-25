import pandas as pd
import qrcode
warnings.filterwarnings('ignore')

def generar_qr( df, columna, nombre_salida):
     """
    Genera un procesamiento para agrupar en un solo archivo distintos archivos tabulares csv.

    Parámetros
    ----------
    df : dataframe
        dataframe que contiene los datos.
    columna : str
        columna con clave unica con la que se generaran los códigos QR.
    nombre_salida :  str
        Sufijo de salida para el archivo

    Regresa
    -------
    png
        Imagenes png de los archivos QR de las columnas de interes
    """
    cve = df[columna]
    
    for i in cve:
        img = qrcode.make(i)
        img.save(f'{nombre_salida}_{i}.png')
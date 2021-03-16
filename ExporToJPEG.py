import arcpy, os 

#Define la carperta a partir en la que se encuentran los archivos que quieres exportar

arcpy.env.workspace = ws = r"C:\\My_Folder" 


mxd_list = arcpy.ListFiles("*.mxd")

#Los archivos se guardan en la misma carpeta, el proceso es un poco tardado

for mxd in mxd_list:
    
    current_mxd = arcpy.mapping.MapDocument(os.path.join(ws, mxd))
    jpeg_name = mxd[:-4] + ".jpg"
    arcpy.mapping.ExportToJPEG(current_mxd, jpeg_name, resolution=300)
 
del mxd_list
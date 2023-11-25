from mmqgis.mmqgis_library import *

'''

Este script exporta el kml con estilos de las capas vectoriales de un proyecto de Qgis
Es necesario tener el proyecto abierto
Es necesario tener activos las capas que se deseén exportar
Cambiar paths de donde se guarda el archivo

'''


self=qgis.utils
layers = self.iface.mapCanvas().layers()
layer_tree_view = iface.layerTreeView()
layers = self.iface.mapCanvas().layers()
print (layers)

#Definimos la ruta donde se guardan los kml
directorio = "C:/Style/KML/"

for layer in layers:
    layerType = layer.type()
    if layerType == QgsMapLayer.VectorLayer:
        g =layer_tree_view.setCurrentLayer(layer)
        group = layer_tree_view.currentGroupNode().name()
        print (group)
        print("--------------")
        print ("layer: " + str(layer))
        print("     input_layer")
        input_layer_name = layer.name()
        input_layer_name_1 = str(input_layer_name ) + ".gpkg"
        print("input_layer_name: " + str(input_layer_name))
        #input_layer = QgsVectorLayer(input_layer_name)
        input_layer = layer
        print ("input layer: " + str(input_layer))
        print("--------------")
        #Obtener nombre del campo
        name_field = ""
        for index, field in enumerate(layer.fields()):
            if ( index == 0):
                name_field = field.name()
                print("campo: " + str(name_field))
            
        print("--------------")
        #Obtener la descripción de las columnas dentro del layer
        description = ""
        for index, field in enumerate(layer.fields()):
            if (index == 0):
                description = "<p>"
                
            else:
                description = description + ', '

            description = description + '{{' + field.name() + '}}'

            if (index == (len(layer.fields()) - 1)):
                description = description + "</p>"
        print(description)
    
        print("--------------")
    
        export_data = True
    
        print("--------------")
    
        output_file_name = f"{directorio}{group}_{input_layer_name}.kml"
        print (output_file_name)
    
        message = mmqgis_kml_export(input_layer, name_field, description,export_data, output_file_name)
    
        print("KML Export From a Project File: " + str(message))
    
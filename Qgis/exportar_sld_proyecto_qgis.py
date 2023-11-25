import processing
'''
Este script exporta los estilos de las capas de un proyecto de qgis
Es necesario correrlo desde el proyecto abierto de Qgis
Cambiar los paths de donde quieres guardar el archivo

'''

self=qgis.utils

layers = iface.mapCanvas().layers()
layer_tree_view = iface.layerTreeView()

for layer in layers:
    g =layer_tree_view.setCurrentLayer(layer)
    print (g)
    group = layer_tree_view.currentGroupNode().name()
    print (group)
    #print(layer_tree_view.currentGroupNode().name())
    name = layer.name()
    print (name)
    # Imprime el nombre de la capa solo si la capa no se encuentra en un grupo
    if group == '':
        pathsld = 'C:/Style/SLD/'+str(name)+'.sld' 
       
    # Imprime el nombre de la capa + el nombre del grupo en el que se encuentra
    else :
        pathsld = 'C:/Style/SLD/'+ str(group) +'__' +str(name)+'.sld'
        
    layer.saveSldStyle(pathsld)
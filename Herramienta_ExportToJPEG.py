import arcpy, sys, os, string 

mxdList = string.split(arcpy.GetParameterAsText(0), ";") 

outloc = arcpy.GetParameterAsText(1)

for item in mxdList: 
	
	item = item.strip('\'') 
	
	mxd = arcpy.mapping.MapDocument(item) 
	
	base = os.path.basename(item) 
	
	base = os.path.splitext(base)[0] + os.path.splitext(base)[1] 
	
	mxd.ExportToJPEG(outloc + os.sep + base, resolution=100)
	
	arcpy.AddMessage(os.path.basename(item) + " has been exported")
	

import arcpy
arcpy.env.workspace = r"E:\TaxMapsProject\Image File Folders\Tax Maps 2013\Anne2013"
arcpy.env.overwriteOutput = True

#Get list of files in Joined folder
fileList = arcpy.ListRasters(wild_card=None, raster_type="TIF")
print fileList

#Set raster as basis for coordinate system
for file in fileList:
    try:
        spatial_ref = arcpy.Describe(file).spatialReference
        print spatial_ref.name
    except:
        print "error"

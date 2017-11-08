from arcpy import ListRasters
from arcpy import env
from arcpy import GetRasterProperties_management

env.workspace = r"E:\TaxMapsProject\Image File Folders\Tax Maps 2013\Alle2013"
env.overwriteOutput = True

#Get list of files in Joined folder
fileList = ListRasters(wild_card=None, raster_type="TIF")
print fileList

#Set raster as basis for coordinate system
for file in fileList:
    try:
        strValueType = GetRasterProperties_management(in_raster=file,property_type="VALUETYPE")
        print "Bit Depth: {}".format(strValueType)
    except:
        print "error"

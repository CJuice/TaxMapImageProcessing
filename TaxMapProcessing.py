"""
Evaluate .tif images for an accompanying .tfw file, the bit depth, and projection. Writes a report .csv with findings.

Completes step 2 of a 2 step process as of 20171109.
Imports ImageClass.py.
Gathers two paths from the user using raw_input.
    path 1 is the directory for the consolidated image files evaluated in step 1
    path 2 is the geodatabase workspace for re-projected images and a raster catalog
Defines the projection for each image, re-projects the image, re-locates the image to the workspace,
creates a raster catalog, and loads the images into a raster catalog.
ASSUMPTIONS:  All files have been run through the Step 1 process. All TIF images have a TFW.
Author: CJS
Date: 20171108
"""

#TODO: once script stabilizes refine imports to slim imported content
#TODO: See if decorators can be used to reduce redundant error catching code

# IMPORTS
import os
from sys import exit
from arcpy import management
from arcpy import env
from arcpy import SpatialReference
from arcpy import GetMessages
from arcpy import ExecuteError
from datetime import date
import ImageClass
from UtilityClass import UtilityClassFunctionality

# VARIABLES
strDateToday = str(date.today()).replace("-", "")
strConsolidatedImageFileFolderPath = None
strGeodatabaseWorkspacePath = None
lsTifFilesInImagesFolder = None
intDefineProjectionCode = 26985 # WKID 2248 is feet, WKID 26985 is meters
intProjectRasterCode = 3857 # WKID 3857 is web mercator
objSpatialReferenceProjectedRaster = SpatialReference(intProjectRasterCode)
# strRasterDatasetName = "RD_{}".format(strDateToday)
strRasterCatalogName = "RCmanaged_{}".format(strDateToday)
lsImageObjects = []
lsUnsuccessfulImageReProjections = []

# INPUTS
    # Get the path for the consolidated images files folder
strPromptForConsolidatedImageFileFolderPath = "Paste the path to the folder containing the consolidated image files.\n>"
strConsolidatedImageFileFolderPath = UtilityClassFunctionality.rawInputBasicChecks(strPromptForConsolidatedImageFileFolderPath)

    # Get the geodatabase workspace from the user
strPromptForGeodatabaseWorkspacePath = "Paste the path to the workspace (geodatabase).\n>"
strGeodatabaseWorkspacePath = UtilityClassFunctionality.rawInputBasicChecks(strPromptForGeodatabaseWorkspacePath)

# FUNCTIONALITY
    # Functions
@UtilityClassFunctionality.captureAndPrintGeoprocessingErrors
def runESRIGPTool(func, *args, **kwargs):
    return func(*args, **kwargs)

    # See if workspace exists
try:
    if os.path.exists(strGeodatabaseWorkspacePath):
        print "gdb exists"
        # assign workspace to env variable and set overwrite output to true
        env.workspace = strGeodatabaseWorkspacePath
        env.overwriteOutput = True
    else:
        print "The workspace is invalid."
        exit()
except Exception as e:
    print "Error in checking workspace path existence.\n{}".format(e)
    exit()

try:
    for (dirname, dirs, files) in os.walk(strConsolidatedImageFileFolderPath):
        for eachFile in files:
            if (str(eachFile)).endswith("tif"):

                # Build image object, set properties, and store in list
                objImage = ImageClass.Image(dirname, str(eachFile))
                objImage.setFileName_lower()
                print "Defining projection... {}".format(objImage.getFileName_lower())
                runESRIGPTool(management.DefineProjection,
                              in_dataset=objImage.getFilePath_Original(),
                              coor_system=intDefineProjectionCode)
                print "Re-Projecting... {}".format(objImage.getFileName_lower())
                runESRIGPTool(management.ProjectRaster,
                              in_raster=objImage.getFilePath_Original(),
                              out_raster=objImage.getFileName_lower(),
                              out_coor_system=objSpatialReferenceProjectedRaster,
                              resampling_type=None,
                              cell_size=None,
                              geographic_transform="NAD_1983_To_WGS_1984_1",
                              Registration_Point=None,
                              in_coor_system=None)
                #TODO: lost the below functionality when I went to Decorator use
                #     lsUnsuccessfulImageReProjections.append(objImage.getFileName_lower())
            else:
                continue
except Exception as e:
    print "Error walking directory and creating Image object.\n{}".format(e)
    exit()

runESRIGPTool(management.CreateRasterCatalog,
              out_path=env.workspace,
              out_name=strRasterCatalogName,
              raster_spatial_reference=objSpatialReferenceProjectedRaster,
              spatial_reference=objSpatialReferenceProjectedRaster,
              config_keyword=None,
              spatial_grid_1=0,
              spatial_grid_2=0,
              spatial_grid_3=0,
              raster_management_type="MANAGED",
              template_raster_catalog=None)

print "Loading workspace into raster catalog..."

    # Load raster datasets into raster catalog
runESRIGPTool(management.WorkspaceToRasterCatalog,
              env.workspace,
              strRasterCatalogName,
              include_subdirectories=None,
              project=None)

print "Process complete."
# if len(lsUnsuccessfulImageReProjections) != 0:
#     print "The following list of lowercase filenames did not Re-Project\n{}".format(lsUnsuccessfulImageReProjections)
# else:
#     pass

# DELETIONS

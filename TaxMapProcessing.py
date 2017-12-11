"""
Evaluate .tif images for an accompanying .tfw file, the bit depth, and projection. Writes a report .csv with findings.

Completes step 2 of a 2 step process as of 20171109.
ASSUMPTIONS:  All files have been run through the Step 1 process. All TIF images have a TFW.
Imports ImageClass.py and UtilityClass.py
Gathers two paths from the user using raw_input.
    path 1 is the directory for the consolidated image files evaluated in step 1
    path 2 is the geodatabase workspace for re-projected images and a raster catalog
Step through the consolidated image directory.
Create Image Objects for all files.
Defines the projection for each image, re-projects the image, and re-locates the image to the workspace.
Creates a raster catalog.
Loads the images into the raster catalog.
Alert user to images that did not reproject
Author: CJS
Date: 20171108
"""
# IMPORTS
import os
from sys import exit
from arcpy import management
from arcpy import env
from arcpy import SpatialReference
import datetime
from datetime import date
import ImageClass
from UtilityClass import UtilityClassFunctionality
import logging
    # importing below so that decorator method does not have to import on first use
from arcpy import GetMessages
from arcpy import ExecuteError

# VARIABLES
    # General
strDateTodayNoDashes = str(date.today()).replace("-", "")
strConsolidatedImageFileFolderPath = None
strGeodatabaseWorkspacePath = None
lsTifFilesInImagesFolder = None
intDefineProjectionCode = 26985 # WKID 2248 is feet, WKID 26985 is meters
intProjectRasterCode = 3857 # WKID 3857 is web mercator
objSpatialReferenceProjectedRaster = SpatialReference(intProjectRasterCode)
strRasterCatalogName = "RCmanaged_{}".format(strDateTodayNoDashes)
env.overwriteOutput = True
strPSADefiningProjection = "Defining projection... {}"
strPSAReProjecting = "Re-Projecting... {}"
strPSAWorkspaceToRasterCatalog = "Loading workspace into raster catalog..."
strPSAProcessComplete = "Process complete."
strPSAListOfFailedReProjections = "The following list of lowercase filenames did not Re-Project\n{}"
strGeographicTransformationNAD83_WGS84 = "NAD_1983_To_WGS_1984_1"
strRasterManagementType = "MANAGED"
    # Input prompt messages
strPromptForConsolidatedImageFileFolderPath = "Paste the path to the folder containing the consolidated image files.\n>"
strPromptForGeodatabaseWorkspacePath = "Paste the path to the workspace (geodatabase).\n>"
    # Error messages
strErrorMsgPathInvalid = "Path does not appear to exist. \n{}\n"
strErrorMsgWalkingDirectoryAndObjectCreationFail = "Error walking directory and creating Image object.\n{}"
    # Lists
lsImageObjects = []
lsUnsuccessfulImageReProjections = []
    # Logging setup
strInfo = "info"
strWarning = "warning"
strError = "error"
strLogFileName = "LOG_TaxMapProcessing.log"
tupTodayDateTime = datetime.datetime.utcnow().timetuple()
strTodayDateTimeForLogging = "{}/{}/{} UTC[{}:{}:{}]".format(tupTodayDateTime[0]
                                                          , tupTodayDateTime[1]
                                                          , tupTodayDateTime[2]
                                                          , tupTodayDateTime[3]
                                                          , tupTodayDateTime[4]
                                                          , tupTodayDateTime[5])
logging.basicConfig(filename=strLogFileName,level=logging.INFO)
logging.info(" {} - Initiated Processing".format(strTodayDateTimeForLogging))

# INPUTS
    # Get the path for the consolidated images files folder
try:
    strConsolidatedImageFileFolderPath = UtilityClassFunctionality.rawInputBasicChecks(strPromptForConsolidatedImageFileFolderPath)
    UtilityClassFunctionality.checkPathExists(strConsolidatedImageFileFolderPath)
except:
    UtilityClassFunctionality.printAndLog(strErrorMsgPathInvalid.format(strConsolidatedImageFileFolderPath), strError)
    exit()

    # Get the geodatabase workspace from the user. if valid set workspace.
try:
    strGeodatabaseWorkspacePath = UtilityClassFunctionality.rawInputBasicChecks(strPromptForGeodatabaseWorkspacePath)
    UtilityClassFunctionality.checkPathExists(strGeodatabaseWorkspacePath)
    env.workspace = strGeodatabaseWorkspacePath
except:
    UtilityClassFunctionality.printAndLog(strErrorMsgPathInvalid.format(strGeodatabaseWorkspacePath), strError)
    exit()

# FUNCTIONS
@UtilityClassFunctionality.captureAndPrintGeoprocessingErrors
def runESRIGPTool(func, *args, **kwargs):
    """Pass ESRI geoprocessing function and arguements through Decorator containing error handling functionality"""

    return func(*args, **kwargs)

# FUNCTIONALITY
    # Step through the consolidated image directory.
    # Create Image Objects for all files.
    # Define Projection
    # Project Raster
try:
    for (dirname, dirs, files) in os.walk(strConsolidatedImageFileFolderPath):
        for eachFile in files:
            if (str(eachFile)).endswith("tif"):

                # Build image object, set properties, and store in list
                objImage = ImageClass.Image(dirname, str(eachFile),strConsolidatedImageFileFolderPath)
                objImage.setFileName_lower()
                UtilityClassFunctionality.printAndLog(strPSADefiningProjection.format(objImage.getFileName_lower()), strInfo)

                # Define Projection
                runESRIGPTool(management.DefineProjection,
                              in_dataset=objImage.getFilePath_Original(),
                              coor_system=intDefineProjectionCode)
                UtilityClassFunctionality.printAndLog(strPSAReProjecting.format(objImage.getFileName_lower()), strInfo)

                # Project Raster
                try:
                    runESRIGPTool(management.ProjectRaster,
                                  in_raster=objImage.getFilePath_Original(),
                                  out_raster=objImage.getFileName_lower(),
                                  out_coor_system=objSpatialReferenceProjectedRaster,
                                  resampling_type=None,
                                  cell_size=None,
                                  geographic_transform=strGeographicTransformationNAD83_WGS84,
                                  Registration_Point=None,
                                  in_coor_system=None)
                except:
                    lsUnsuccessfulImageReProjections.append(objImage.getFileName_lower())
            else:
                continue
except Exception as e:
    UtilityClassFunctionality.printAndLog(strErrorMsgWalkingDirectoryAndObjectCreationFail.format(e), strError)
    exit()

    # Create Raster Catalog
runESRIGPTool(management.CreateRasterCatalog,
              out_path=env.workspace,
              out_name=strRasterCatalogName,
              raster_spatial_reference=objSpatialReferenceProjectedRaster,
              spatial_reference=objSpatialReferenceProjectedRaster,
              config_keyword=None,
              spatial_grid_1=0,
              spatial_grid_2=0,
              spatial_grid_3=0,
              raster_management_type=strRasterManagementType,
              template_raster_catalog=None)

UtilityClassFunctionality.printAndLog(strPSAWorkspaceToRasterCatalog, strInfo)

    # Load raster datasets into raster catalog
runESRIGPTool(management.WorkspaceToRasterCatalog,
              env.workspace,
              strRasterCatalogName,
              include_subdirectories=None,
              project=None)

    # Alert user to images that did not reproject
if len(lsUnsuccessfulImageReProjections) != 0:
    UtilityClassFunctionality.printAndLog(strPSAListOfFailedReProjections.format(lsUnsuccessfulImageReProjections), strInfo)
else:
    pass

UtilityClassFunctionality.printAndLog(strPSAProcessComplete, strInfo)
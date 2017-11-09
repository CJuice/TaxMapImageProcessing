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
strConsolidatedImageFileFolderPath = raw_input("Paste the path to the folder containing the consolidated image files.\n>")

    # Get the geodatabase workspace from the user
strGeodatabaseWorkspacePath = raw_input("Paste the path to the workspace (geodatabase).\n>")

# FUNCTIONALITY
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
                try:
                    management.DefineProjection(in_dataset=objImage.getFilePath_Original(),
                                                coor_system=intDefineProjectionCode)
                except ExecuteError:
                    print "Geoprocessing error during Define Projection for image {}.\n{}".format(objImage.getFileName_lower(),GetMessages(2))
                except Exception as e:
                    print e

                print "Define Projection successful"
                print "Re-Projecting... {}".format(objImage.getFileName_lower())
                try:
                    management.ProjectRaster(in_raster=objImage.getFilePath_Original(),
                                             out_raster=objImage.getFileName_lower(),
                                             out_coor_system=objSpatialReferenceProjectedRaster,
                                             resampling_type=None,
                                             cell_size=None,
                                             geographic_transform="NAD_1983_To_WGS_1984_1",
                                             Registration_Point=None,
                                             in_coor_system=None)
                    print "Re-Project successful.\n----------"
                except ExecuteError:
                    print "Geoprocessing error during Project Raster for {}. Skipping file.\n{}".format(objImage.getFileName_lower(),GetMessages(2))
                    lsUnsuccessfulImageReProjections.append(objImage.getFileName_lower())
                except Exception as e:
                    print e
            else:
                continue
except Exception as e:
    print "Error walking directory and creating Image object.\n{}".format(e)
    exit()

try:
    # Create Raster Catalog in workspace
    management.CreateRasterCatalog(out_path=env.workspace,
                                   out_name=strRasterCatalogName,
                                   raster_spatial_reference=objSpatialReferenceProjectedRaster,
                                   spatial_reference=objSpatialReferenceProjectedRaster,
                                   config_keyword=None,
                                   spatial_grid_1=0,
                                   spatial_grid_2=0,
                                   spatial_grid_3=0,
                                   raster_management_type="MANAGED",
                                   template_raster_catalog=None)
except ExecuteError:
    print "Error creating Raster Catalog.\n{}".format(GetMessages(2))
    exit()
except Exception as e:
    print e
    exit()

print "Loading workspace into raster catalog..."

    # Load raster datasets into raster catalog
try:
    management.WorkspaceToRasterCatalog(env.workspace,
                                        strRasterCatalogName,
                                        include_subdirectories=None,
                                        project=None)
except ExecuteError:
    print "Geoprocessing error loading workspace into {}.\n{}".format(strRasterCatalogName,GetMessages(2))
    exit()
except Exception as e:
    print e
    exit()

print "Process complete."
if len(lsUnsuccessfulImageReProjections) != 0:
    print "The following list of lowercase filenames did not Re-Project\n{}".format(lsUnsuccessfulImageReProjections)
else:
    pass

# DELETIONS

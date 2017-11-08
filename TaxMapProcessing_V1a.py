####################
# Author: CJS
# Date: 20171108
#
#
#
# ASSUMPTIONS:  All files have been run through the Step 1 process.
#               All TIF images have a TFW.
####################
#TODO: once script stabilizes refine imports to slim imported content
# IMPORTS
import os
from sys import exit
from arcpy import management
from arcpy import env
from arcpy import SpatialReference
from arcpy import GetMessages
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
except:
    print "Error in checking workspace path existence. Exiting."
    exit()

print "Defining projection..."

try:
    for (dirname, dirs, files) in os.walk(strConsolidatedImageFileFolderPath):
        for file in files:
            if (str(file)).endswith("tif"):
                # Build image object, set properties, and store in list
                objImage = ImageClass.Image(dirname, str(file))
                objImage.setFileName_lower()
                print "Defining projection... {}".format(objImage.getFileName_lower())
                management.DefineProjection(in_dataset=objImage.getFilePath_Original(),
                                            coor_system=intDefineProjectionCode)
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
                    print "Re-Project successful."
                except:
                    print "Project unsuccessful for {}. Skipping file.".format(objImage.getFileName_lower())
                    lsUnsuccessfulImageReProjections.append(objImage.getFileName_lower())
            else:
                continue
except:
    print "Error walking directory and creating Image object."
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
except:
    print "Error creating Raster Catalog"
    print(GetMessages())
    exit()

print "Loading workspace into raster catalog..."
    # Load raster datasets into raster catalog
try:
    management.WorkspaceToRasterCatalog(env.workspace,
                                        strRasterCatalogName,
                                        include_subdirectories=None,
                                        project=None)
except:
    print "Error loading workspace into {}".format(strRasterCatalogName)
    print(GetMessages())
    exit()

print "Process complete."
if len(lsUnsuccessfulImageReProjections) != 0:
    print "The following list of lowercase filenames unsuccessfully Re-Projected\n{}".format(lsUnsuccessfulImageReProjections)
else:
    pass

# DELETIONS

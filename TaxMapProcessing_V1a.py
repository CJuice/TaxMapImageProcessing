####################
#
#
#
#
#
#
####################
#TODO: once script stabilizes refine imports to slim imported content
# IMPORTS
import os
from sys import exit
from arcpy import management
from arcpy import env
from arcpy import SpatialReference
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
strRasterDatasetName = "RD_{}".format(strDateToday)
strRasterCatalogName = "RCmanaged_{}".format(strDateToday)
lsImageObjects = []

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

    # Create Raster Dataset in workspace
print "Creating Raster Dataset in Workspace"
try:
    management.CreateRasterDataset(out_path=env.workspace,
                                   out_name=strRasterDatasetName,
                                   cellsize=None,
                                   pixel_type="1_BIT",
                                   raster_spatial_reference=intProjectRasterCode,
                                   number_of_bands=1,
                                   config_keyword=None,
                                   pyramids=None,
                                   tile_size=None,
                                   compression=None,
                                   pyramid_origin=None)
except:
    print "Error creating raster dataset. Exiting."

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

    # Define projection and reproject the rasters

env.workspace = os.path.join(env.workspace,strRasterDatasetName)
print "Switching workspace to {}.".format(env.workspace)
print "Define projection and re-projection underway..."

#TODO: Run this again, determine why a Raster Dataset did not show in the gdb and also why it errored out and exited below.
#TODO: Why are the rasters I'm projecting showing as a file in the gdb instead of being inside the RD I precreated!?
try:
    for (dirname, dirs, files) in os.walk(strConsolidatedImageFileFolderPath):
        print 1
        for file in files:
            print 2
            if (str(file)).endswith("tif"):
                print 3
                # Build image object, set properties, and store in list
                objImage = ImageClass.Image(dirname, str(file))
                print 4
                objImage.setFileName_lower()
                print 5
                management.DefineProjection(in_dataset=objImage.getFilePath_Original(),
                                            coor_system=intDefineProjectionCode)
                print "Define Projection successful: {}".format(objImage.getFileName_lower())
                #TODO: If all tif.xml files prove to be the same then simply make a copy of the first xml file created by the Define Projection tool and rename new copy for each TIF
                management.ProjectRaster(in_raster=objImage.getFilePath_Original(),
                                         out_raster=objImage.getFileName_lower(),
                                         out_coor_system=objSpatialReferenceProjectedRaster,
                                         resampling_type=None,
                                         cell_size=None,
                                         geographic_transform="NAD_1983_To_WGS_1984_1",
                                         Registration_Point=None,
                                         in_coor_system=None)
                print "Project successful: {}".format(objImage.getFileName_lower())
            else:
                continue
except:
    print "Error walking directory and creating Image object."
    exit()
# try:
#     for(dirname, dirs, files) in os.walk(strConsolidatedImageFileFolderPath):
#         for file in files:
#             strFileName = str(file)
#             if strFileName.endswith("tif"):
#                 print strFileName
#                 strFileNameWithoutTifExtension = strFileName.rstrip(".tif")
#                 strFilePath = os.path.join(dirname,strFileName)
#                 management.DefineProjection(in_dataset=strFilePath,
#                                             coor_system=intDefineProjectionCode)
#                 print "Define Projection successful: {}".format(strFileName)
#                 management.ProjectRaster(in_raster=strFilePath,
#                                          out_raster=strFileNameWithoutTifExtension,
#                                          out_coor_system=objSpatialReferenceProjectedRaster,
#                                          resampling_type=None,
#                                          cell_size=None,
#                                          geographic_transform="NAD_1983_To_WGS_1984_1",
#                                          Registration_Point=None,
#                                          in_coor_system=None)
#                 print "Project successful: {}".format(strFileName)
#             else:
#                 continue
# except:
#     print "Error in projection process. Exiting."
#     exit()
    # Load raster dataset into raster catalog
try:
    print "Now loading raster dataset into raster catalog..."
    management.WorkspaceToRasterCatalog(env.workspace,
                                        strRasterCatalogName,
                                        include_subdirectories=None,
                                        project=None)
except:
    print "Error loading raster dataset into raster catalog"
# DELETIONS

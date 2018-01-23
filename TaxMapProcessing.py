"""
Evaluate .tif images for an accompanying .tfw file, the bit depth, and projection. Writes a report .csv with findings.

Completes step 2 of a 2 step process as of 20171109.
ASSUMPTIONS:  All files have been run through the Step 1 process. All TIF images have a TFW.
Imports ImageClass.py, UtilityClass.py, TaxMapVariables.py
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
def main(ConsolidatedImageFileFolderPath=None,GeodatabaseWorkspacePath=None):
    # IMPORTS
    import os
    from sys import exit
    from arcpy import management
    from arcpy import env
    import ImageClass
    from UtilityClass import UtilityClassFunctionality
    import logging
    import TaxMapVariables as myvars

        # importing below so that decorator method does not have to import on first use
    from arcpy import GetMessages
    from arcpy import ExecuteError

    # ARCPY ENVIRONMENT SETTING
    env.overwriteOutput = True

    # LOGGING SETUP
    logging.basicConfig(filename=myvars.strLogFileName,level=logging.INFO)
    UtilityClassFunctionality.printAndLog(" {} - Initiated Processing".format(UtilityClassFunctionality.getDateTimeForLoggingAndPrinting()), UtilityClassFunctionality.INFO_LEVEL)

    # INPUTS
        # Get the path for the consolidated images files folder
    try:
        if ConsolidatedImageFileFolderPath == None:
            strConsolidatedImageFileFolderPath = UtilityClassFunctionality.rawInputBasicChecks(myvars.strPromptForConsolidatedImageFileFolderPath)
        else:
            strConsolidatedImageFileFolderPath = ConsolidatedImageFileFolderPath
        UtilityClassFunctionality.checkPathExists(strConsolidatedImageFileFolderPath)
    except:
        UtilityClassFunctionality.printAndLog(myvars.strErrorMsgPathInvalid.format(strConsolidatedImageFileFolderPath), UtilityClassFunctionality.ERROR_LEVEL)
        exit()

        # Get the geodatabase workspace from the user. if valid set workspace.
    try:
        if GeodatabaseWorkspacePath == None:
            strGeodatabaseWorkspacePath = UtilityClassFunctionality.rawInputBasicChecks(myvars.strPromptForGeodatabaseWorkspacePath)
        else:
            strGeodatabaseWorkspacePath = GeodatabaseWorkspacePath
        UtilityClassFunctionality.checkPathExists(strGeodatabaseWorkspacePath)
        env.workspace = strGeodatabaseWorkspacePath
    except:
        UtilityClassFunctionality.printAndLog(myvars.strErrorMsgPathInvalid.format(strGeodatabaseWorkspacePath), UtilityClassFunctionality.ERROR_LEVEL)
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
                    objImage = ImageClass.Image(dirname, str(eachFile), strConsolidatedImageFileFolderPath)
                    UtilityClassFunctionality.printAndLog(myvars.strPSADefiningProjection.format(objImage.strFileName_lower), UtilityClassFunctionality.INFO_LEVEL)

                    # Define Projection
                    runESRIGPTool(management.DefineProjection,
                                  in_dataset=objImage.strFilePath_Original,
                                  coor_system=myvars.intDefineProjectionCode)
                    UtilityClassFunctionality.printAndLog(myvars.strPSAReProjecting.format(objImage.strFileName_lower), UtilityClassFunctionality.INFO_LEVEL)

                    # Project Raster
                    try:
                        runESRIGPTool(management.ProjectRaster,
                                      in_raster=objImage.strFilePath_Original,
                                      out_raster=objImage.strFileName_lower,
                                      out_coor_system=myvars.objSpatialReferenceProjectedRaster,
                                      resampling_type=None,
                                      cell_size=None,
                                      geographic_transform=myvars.strGeographicTransformationNAD83_WGS84,
                                      Registration_Point=None,
                                      in_coor_system=None)
                    except:
                        myvars.lsUnsuccessfulImageReProjections.append(objImage.strFileName_lower)
                else:
                    continue
    except Exception as e:
        UtilityClassFunctionality.printAndLog(myvars.strErrorMsgWalkingDirectoryAndObjectCreationFail.format(e), UtilityClassFunctionality.ERROR_LEVEL)
        exit()

        # Create Raster Catalog
    runESRIGPTool(management.CreateRasterCatalog,
                  out_path=env.workspace,
                  out_name=myvars.strRasterCatalogName,
                  raster_spatial_reference=myvars.objSpatialReferenceProjectedRaster,
                  spatial_reference=myvars.objSpatialReferenceProjectedRaster,
                  config_keyword=None,
                  spatial_grid_1=0,
                  spatial_grid_2=0,
                  spatial_grid_3=0,
                  raster_management_type=myvars.strRasterManagementType,
                  template_raster_catalog=None)

    UtilityClassFunctionality.printAndLog(myvars.strPSAWorkspaceToRasterCatalog, UtilityClassFunctionality.INFO_LEVEL)

        # Load raster datasets into raster catalog
    runESRIGPTool(management.WorkspaceToRasterCatalog,
                  env.workspace,
                  myvars.strRasterCatalogName,
                  include_subdirectories=None,
                  project=None)

        # Alert user to images that did not reproject
    if len(myvars.lsUnsuccessfulImageReProjections) != 0:
        UtilityClassFunctionality.printAndLog(myvars.strPSAListOfFailedReProjections.format(myvars.lsUnsuccessfulImageReProjections), UtilityClassFunctionality.INFO_LEVEL)
    else:
        pass

    UtilityClassFunctionality.printAndLog(myvars.strPSAProcessComplete, UtilityClassFunctionality.INFO_LEVEL)
if __name__ == '__main__':
    print("NOTICE: Should be run through TaxMapProcessGUI.py. Loading anyway...")
    from UtilityClass import UtilityClassFunctionality
    import TaxMapVariables as myvars

    # strConsolidatedImageFileFolderPath = UtilityClassFunctionality.rawInputBasicChecks(myvars.strPromptForConsolidatedImageFileFolderPath)
    # strGeodatabaseWorkspacePath = UtilityClassFunctionality.rawInputBasicChecks(myvars.strPromptForGeodatabaseWorkspacePath)
    main(None,None)
else:
    pass
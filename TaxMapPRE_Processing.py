"""
Evaluate .tif images for an accompanying .tfw file, the bit depth, and projection. Writes a report .csv with findings.

Completes step 1 of a 2 step process as of 20171109.
Step 1 is the pre-processing step used to check Tax Map Images from the MD Department of Planning
in order to avoid throwing errors later on in Step 2.
The script does the following actions:
Imports UtilityClass.py and ImageClass.py.
Gathers two paths from the user using raw_input.
    path 1 is the directory for the image files
    path 2 is the directory where an output report csv file will be created
Creates a csv file and populates it with data gathered about the images.
Prompts user to move forward after displaying file extensions present in directory.
Creates new directory for relocated images.
Step through the directory and all subdirectories.
Create Image Objects for all files.
Write every image object filename to a list based on the file extension.
Notify the script user of the file extensions they are asking the script to examine and get a decision on proceed/exit;
basically a check for non TIF and TFW files such as zip files.
Step through all Image Objects.
Check that each .tif has a .tfw file and write result to dictionary with filename:(Zero for False, One for True).
Check the bit depth of each .tif .
Check the projection.
Check the units (meters/feet/other).
Check the pixel dimensions.
Each record in report file will have "Filename,HasTFW,BitDepth,Projection,TFW_SuggestedUnit,XY_PixelSize"
Move all files to master location
Build the report data.
Create and Write the report file for use in excel etc.
Provide the user an opportunity to immediately move on to Step 2 after reviewing the report data.
Author: CJS
Date: 20171108
Revisions: 20180118 Refactored code to use @property and reduce bloat
"""
# Imports
from sys import exit
import os
from arcpy import Describe, ExecuteError, GetMessages, management
import shutil
from UtilityClass import UtilityClassFunctionality
import ImageClass
import logging
import TaxMapVariables as myvars

# Logging setup
logging.basicConfig(filename=myvars.strLogFileName,level=logging.INFO)
UtilityClassFunctionality.printAndLog(" {} - Initiated Pre-Processing".format(UtilityClassFunctionality.getDateTimeForLoggingAndPrinting()), UtilityClassFunctionality.INFO_LEVEL)

# INPUTS
    # Get the directory of the tif files to walk through
try:
    strInputFileDirectory = UtilityClassFunctionality.rawInputBasicChecks(myvars.strPromptForImageDirectoryPath)
    UtilityClassFunctionality.checkPathExists(strInputFileDirectory)
except Exception as e:
    UtilityClassFunctionality.printAndLog(myvars.strErrorMsgImageFileDirectoryInvalid.format(e), UtilityClassFunctionality.ERROR_LEVEL)
    exit()

    # Get the path where a new folder will be created. The folder will hold all image files.
try:
    strNewFileDirectoryForAllImages = UtilityClassFunctionality.rawInputBasicChecks(myvars.strPromptForNewImageDirectoryPath)
    if os.path.exists(strNewFileDirectoryForAllImages):
        try:
            strNewFolderNameForAllImagesStorage = "{}{}".format(myvars.strDateTodayNoDashes, myvars.strNewImageFolderEnding)
            strNewMasterImageCollectionFolderPath = os.path.join(strNewFileDirectoryForAllImages, strNewFolderNameForAllImagesStorage)
            os.mkdir(strNewMasterImageCollectionFolderPath)
            strReportFileLocation = strNewMasterImageCollectionFolderPath  # Report file will go in with images
        except Exception as e:
            UtilityClassFunctionality.printAndLog(myvars.strErrorMsgNewFolderCreationFail.format(e), UtilityClassFunctionality.ERROR_LEVEL)
            exit()
    else:
        UtilityClassFunctionality.printAndLog(myvars.strErrorMsgPathInvalid.format(strNewFileDirectoryForAllImages), UtilityClassFunctionality.ERROR_LEVEL)
        exit()
except Exception as e:
    UtilityClassFunctionality.printAndLog(myvars.strErrorMsgNewImageDirectoryInvalidOrExists.format(e), UtilityClassFunctionality.ERROR_LEVEL)
    exit()

# FUNCTIONALITY
    # Step through the directory and all subdirectories.
    # Create Image Objects for all files.
    # Write every image object filename to a list based on the file extension.
    # Notify the script user of the file extensions they are asking the script to examine and get a decision on proceed/exit
        # Basically a check for non TIF and TFW files such as zip files.
try:
    for (dirname, dirs, files) in os.walk(strInputFileDirectory):
        myvars.lsImageObjects = myvars.lsImageObjects + [ImageClass.Image(dirname, str(eachFile), strNewMasterImageCollectionFolderPath) for eachFile in files]
    myvars.setOfFileExtensions = set([objImage.strFileExtension_lower for objImage in myvars.lsImageObjects])
    myvars.lsFileNamesTFW = [objImage.strFileName_lower for objImage in myvars.lsImageObjects if objImage.strFileExtension_lower == "tfw"]
    myvars.lsFileNamesTIF = [objImage.strFileName_lower for objImage in myvars.lsImageObjects if objImage.strFileExtension_lower == "tif"]
    UtilityClassFunctionality.printAndLog(myvars.strFileExtensionsPresentInImageDatasets.format(tuple(myvars.setOfFileExtensions)), UtilityClassFunctionality.INFO_LEVEL)
    strUserCheck = UtilityClassFunctionality.rawInputBasicChecks(myvars.strPromptForProceedWithKnownPresentFileExtensions)
except Exception as e:
    UtilityClassFunctionality.printAndLog(myvars.strErrorMsgWalkingDirectoryCheckingExtensionsFail.format(e), UtilityClassFunctionality.ERROR_LEVEL)
    exit()

    # Check user entry to see if they are okay with the files about to be processed.
UtilityClassFunctionality.processUserEntry_YesNo(strUserCheck)
UtilityClassFunctionality.printAndLog(myvars.strPSA_Processing, UtilityClassFunctionality.INFO_LEVEL)
try:
    for image in myvars.lsImageObjects:

        # Create string for new path, with a lowercase file name for standardizing moved image files, and check for existence to avoid error.
        strFullNewDestinationPathForFile_lowerfilename = os.path.join(strNewMasterImageCollectionFolderPath, image.strFileName_and_Extension.lower())
        if os.path.exists(strFullNewDestinationPathForFile_lowerfilename):
            UtilityClassFunctionality.printAndLog(myvars.strErrorMsgFileAlreadyExistsInLocation.format(image.strFilePath_Original), UtilityClassFunctionality.ERROR_LEVEL)
            exit()
        elif image.strFileExtension_lower in myvars.lsAcceptableExtensionsForImageFilesOfInterest:
            image.strFilePath_Moved = strFullNewDestinationPathForFile_lowerfilename

            # Move all files to master location
            shutil.move(image.strFilePath_Original, image.strFilePath_Moved)
        else:
            continue
except Exception as e:
    UtilityClassFunctionality.printAndLog(myvars.strErrorMsgMovingFilesFail.format(e), UtilityClassFunctionality.ERROR_LEVEL)
    exit()

    # Generate the data for the report
        # Check the TIF to TFW relation. Write result to dictionary with filename:False/True.
myvars.dictTFWCheck = {tifFileName:tifFileName in myvars.lsFileNamesTFW for tifFileName in myvars.lsFileNamesTIF}
        # Build the tuple of file data for the report file
try:
    for image in myvars.lsImageObjects:
        if image.strFileExtension_lower == "tif":
            image.boolHasTFW = myvars.dictTFWCheck.get(image.strFileName_lower)

            # NOTE: For the next two operations the decorator is not used because the process needs to continue even
            #       on error. The report file documents all including Errors.
            # Get the bit depth
            try:
                resBitDepth = management.GetRasterProperties(in_raster=image.strFilePath_Moved,
                                                             property_type="VALUETYPE") # Returns a Results Object
                image.intBitDepth = resBitDepth
                strBitDepth = image.getBitDepthPlainLanguage()
            except ExecuteError:
                UtilityClassFunctionality.printAndLog(myvars.strGPErrorMsgBitDepthCheckFail.format(image.strFileName_lower, GetMessages(2)), UtilityClassFunctionality.WARNING_LEVEL)
                strBitDepth = UtilityClassFunctionality.ERROR_LEVEL
            except Exception as e:
                strBitDepth = UtilityClassFunctionality.ERROR_LEVEL
                UtilityClassFunctionality.printAndLog(e, UtilityClassFunctionality.WARNING_LEVEL)

            # Get the spatial reference
            try:
                spatrefProjectionName = Describe(image.strFilePath_Moved).spatialReference
                strProjectionName = str(spatrefProjectionName.name)
            except ExecuteError:
                UtilityClassFunctionality.printAndLog(myvars.strGPErrorMsgSpatialReferenceCheckFail.format(image.strFileName_lower, GetMessages(2)), UtilityClassFunctionality.WARNING_LEVEL)
                strProjectionName = UtilityClassFunctionality.ERROR_LEVEL
            except Exception as e:
                strProjectionName = UtilityClassFunctionality.ERROR_LEVEL
                UtilityClassFunctionality.printAndLog(e, UtilityClassFunctionality.WARNING_LEVEL)

            # Store TFW contents in list, set X,Y coordinates of upper left corner of image, determine projection units,
            #   and determine pixel dimensions
            if image.boolHasTFW:
                image.storeTFWContentsInList()
                image.setXYCoordinatesUpperLeftCornerOfImageFromTFWList()
                image.detectPossibleProjectionUnitsFromTFWList()
                image.setXYPixelSizeFromTFWList()

            # Build report data tuple (HasTFW, BitDepth, Projection)
            tupFileData = (image.boolHasTFW, strBitDepth, strProjectionName, image.strPossibleUnits, image.strXYPixelSize)
            myvars.dictReportData[image.strFileName_lower] = tupFileData
        else:
            continue
except Exception as e:
    UtilityClassFunctionality.printAndLog(myvars.strErrorMsgBuildingReportFail.format(e), UtilityClassFunctionality.ERROR_LEVEL)

    # Create and Write the report file for use in excel etc.
strReportFileName = "{}{}".format(myvars.strDateTodayNoDashes, myvars.strReportFileEnding)
strReportFilePath = os.path.join(strReportFileLocation, strReportFileName)
try:
    with open(strReportFilePath,'w') as fReportFile:
        fReportFile.write("{},{},{},{},{},{}\n".format(myvars.strFileNameHeader, myvars.strHasTFWHeader, myvars.strBitDepthHeader, myvars.strProjectionHeader, myvars.strFeetVsMetersVsOtherHeader, myvars.strXYPixelSizeHeader))
        for key,value in myvars.dictReportData.iteritems():
            fReportFile.write("{},{},{},{},{},{}\n".format(key, value[0], value[1], value[2], value[3], value[4]))
except Exception as e:
    UtilityClassFunctionality.printAndLog(myvars.strErrorMsgOpeningWritingCSVFileFail.format(e), UtilityClassFunctionality.ERROR_LEVEL)
    exit()

UtilityClassFunctionality.printAndLog(myvars.strPSA_ProcessingCompleteSeeReport.format(strReportFilePath), UtilityClassFunctionality.INFO_LEVEL)
UtilityClassFunctionality.printAndLog(myvars.strPSA_ConsolidatedImageFilesLocation.format(strNewMasterImageCollectionFolderPath), UtilityClassFunctionality.INFO_LEVEL)

# Provide the user an opportunity to immediately move on to Step 2 after reviewing the report data.
try:
    strPromptForUserChoiceToContinueToStep2 = myvars.strPSA_MoveToStepTwoProcess
    strContinue = UtilityClassFunctionality.rawInputBasicChecks(strPromptForUserChoiceToContinueToStep2)
    if strContinue.lower() == myvars.strPSA_YESResponseToMoveToStepTwo:
        import TaxMapProcessing
    else:
        UtilityClassFunctionality.printAndLog(myvars.strPSAProcessComplete, UtilityClassFunctionality.INFO_LEVEL)
except Exception as e:
    UtilityClassFunctionality.printAndLog(e, UtilityClassFunctionality.ERROR_LEVEL)
    exit()
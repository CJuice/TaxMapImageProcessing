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
from datetime import date
from UtilityClass import UtilityClassFunctionality
import ImageClass
import logging

# VARIABLES
    # General
strNewImageFolderEnding = "_AllTaxMapImages"
strReportFileEnding = "_TaxMapReportFile.csv"
strFileExtensionsPresentInImageDatasets = "File extensions present in image datasets: {}"
strPSA_Processing = "Processing..."
strPSA_ProcessingCompleteSeeReport = "Pre-Processing Complete. Please visit your report and review the contents.\n\n\tREPORT LOCATION > {}\n"
strPSA_ConsolidatedImageFilesLocation = "\tCONSOLIDATED IMAGE FILES PATH > {}\n"
strPSA_MoveToStepTwoProcess = "If the images files looks satisfactory, based on the report findings, type a 'y' to run Step 2 now. Type 'n' to stop.\n>"
strPSA_YESResponseToMoveToStepTwo = "y"
strPSAProcessComplete = "Process complete."
strDateTodayNoDashes = str(date.today()).replace("-", "")
    # Report file headers
strFileNameHeader = "Filename_lowercase"
strHasTFWHeader = "HasTFW"
strBitDepthHeader = "BitDepth"
strProjectionHeader = "Projection"
strFeetVsMetersVsOtherHeader = "TFW_SuggestedUnit"
strXYPixelSizeHeader = "XY_PixelSize"
    # Input prompt messages
strPromptForImageDirectoryPath = "Paste the path for the directory of .tif files you want to process\n>"
strPromptForNewImageDirectoryPath = "Paste the path where a new folder will be created and will hold a copy of all images for processing\n>"
strPromptForProceedWithKnownPresentFileExtensions = "Proceed? (y/n)\n>"
    # Error messages
strErrorMsgPathDoesNotExist = "Path does not exist."
strErrorMsgImageFileDirectoryInvalid = "Image file directory appears to be invalid.\n{}"
strErrorMsgNewFolderCreationFail = "Error creating new folder.\n{}"
strErrorMsgNewImageDirectoryInvalidOrExists = "The new directory appears to be invalid or already exists.\n{}"
strErrorMsgWalkingDirectoryCheckingExtensionsFail = "Error walking directory and checking file extensions.\n{}"
strErrorMsgFileAlreadyExistsInLocation = "File [{}] already exists in new location."
strErrorMsgMovingFilesFail = "Error while moving files.\n{}"
strGPErrorMsgBitDepthCheckFail = "Geoprocessing error during image {} bit depth check: {}"
strGPErrorMsgSpatialReferenceCheckFail = "Geoprocessing error during image {} spatial reference check: {}"
strErrorMsgBuildingReportFail = "Error while building report data.\n{}"
strErrorMsgOpeningWritingCSVFileFail = "Error opening/writing to report file.\n{}"
    # Lists
lsImageObjects = []
lsAcceptableExtensionsForImageFilesOfInterest = ["tif","tfw","tif.xml"]
lsFileNamesTIF = []
lsFileNamesTFW = []
dictTFWCheck = {}
    # Logging setup
strLogFileName = "LOG_TaxMapProcessing.log"
logging.basicConfig(filename=strLogFileName,level=logging.INFO)
UtilityClassFunctionality.printAndLog(" {} - Initiated Pre-Processing".format(UtilityClassFunctionality.getDateTimeForLoggingAndPrinting()), UtilityClassFunctionality.INFO_LEVEL)

# INPUTS
    # Get the directory of the tif files to walk through
try:
    strInputFileDirectory = UtilityClassFunctionality.rawInputBasicChecks(strPromptForImageDirectoryPath)
    UtilityClassFunctionality.checkPathExists(strInputFileDirectory)
except Exception as e:
    UtilityClassFunctionality.printAndLog(strErrorMsgImageFileDirectoryInvalid.format(e), UtilityClassFunctionality.ERROR_LEVEL)
    exit()

    # Get the path where a new folder will be created. The folder will hold all image files.
try:
    strNewFileDirectoryForAllImages = UtilityClassFunctionality.rawInputBasicChecks(strPromptForNewImageDirectoryPath)
    if os.path.exists(strNewFileDirectoryForAllImages):
        try:
            strNewFolderNameForAllImagesStorage = "{}{}".format(strDateTodayNoDashes, strNewImageFolderEnding)
            strNewMasterImageCollectionFolderPath = os.path.join(strNewFileDirectoryForAllImages, strNewFolderNameForAllImagesStorage)
            os.mkdir(strNewMasterImageCollectionFolderPath)
            strReportFileLocation = strNewMasterImageCollectionFolderPath  # Report file will go in with images
        except Exception as e:
            UtilityClassFunctionality.printAndLog(strErrorMsgNewFolderCreationFail.format(e), UtilityClassFunctionality.ERROR_LEVEL)
            exit()
    else:
        UtilityClassFunctionality.printAndLog(strErrorMsgPathDoesNotExist, UtilityClassFunctionality.ERROR_LEVEL)
        exit()
except Exception as e:
    UtilityClassFunctionality.printAndLog(strErrorMsgNewImageDirectoryInvalidOrExists.format(e), UtilityClassFunctionality.ERROR_LEVEL)
    exit()

# FUNCTIONALITY
    # Step through the directory and all subdirectories.
    # Create Image Objects for all files.
    # Write every image object filename to a list based on the file extension.
    # Notify the script user of the file extensions they are asking the script to examine and get a decision on proceed/exit
        # Basically a check for non TIF and TFW files such as zip files.
try:
    setOfFileExtensions = set()
    for (dirname, dirs, files) in os.walk(strInputFileDirectory):
        for eachFile in files:
            # Build image object, store in list, and set properties
            objImage = ImageClass.Image(dirname, str(eachFile), strNewMasterImageCollectionFolderPath)
            lsImageObjects.append(objImage)
            setOfFileExtensions.add(objImage.strFileExtension_lower)

            # Build list of TIF and TFW files for later use
            if objImage.strFileExtension_lower == "tfw":
                lsFileNamesTFW.append(objImage.strFileName_lower)
            elif objImage.strFileExtension_lower == "tif":
                lsFileNamesTIF.append(objImage.strFileName_lower)
            else:
                continue
    UtilityClassFunctionality.printAndLog(strFileExtensionsPresentInImageDatasets.format(tuple(setOfFileExtensions)), UtilityClassFunctionality.INFO_LEVEL)
    strUserCheck = UtilityClassFunctionality.rawInputBasicChecks(strPromptForProceedWithKnownPresentFileExtensions)
except Exception as e:
    UtilityClassFunctionality.printAndLog(strErrorMsgWalkingDirectoryCheckingExtensionsFail.format(e), UtilityClassFunctionality.ERROR_LEVEL)
    exit()

    # Check user entry to see if they are okay with the files about to be processed.
UtilityClassFunctionality.processUserEntry_YesNo(strUserCheck)
UtilityClassFunctionality.printAndLog(strPSA_Processing, UtilityClassFunctionality.INFO_LEVEL)

    # Step through all Image Objects.
    #   Check that each .tif has a .tfw file and write result to dictionary with filename:(Zero for False, One for True).
    #   Check the bit depth of each .tif .
    #   Check the projection.
    #   Check the TFW units
    #   Check the xy pixel size
    # Move all files to master location
try:
    for image in lsImageObjects:

        # Create string for new path, with a lowercase file name for standardizing moved image files, and check for existence to avoid error.
        strFullNewDestinationPathForFile_lowerfilename = os.path.join(strNewMasterImageCollectionFolderPath, image.strFileName_and_Extension.lower())
        if os.path.exists(strFullNewDestinationPathForFile_lowerfilename):
            UtilityClassFunctionality.printAndLog(strErrorMsgFileAlreadyExistsInLocation.format(image.strFilePath_Original), UtilityClassFunctionality.ERROR_LEVEL)
            exit()
        elif image.strFileExtension_lower in lsAcceptableExtensionsForImageFilesOfInterest:
            image.strFilePath_Moved = strFullNewDestinationPathForFile_lowerfilename
            shutil.move(image.strFilePath_Original, image.strFilePath_Moved)
        else:
            continue
except Exception as e:
    UtilityClassFunctionality.printAndLog(strErrorMsgMovingFilesFail.format(e), UtilityClassFunctionality.ERROR_LEVEL)
    exit()

    # Build the report data
        # Check the TIF to TFW relation
for tifFileName in lsFileNamesTIF:
    if tifFileName in lsFileNamesTFW:
        dictTFWCheck[tifFileName] = True
    else:
        dictTFWCheck[tifFileName] = False

        # Build the tuple of file data for the report file
dictReportData = {}
try:
    for image in lsImageObjects:
        if image.strFileExtension_lower == "tif":
            image.boolHasTFW = dictTFWCheck.get(image.strFileName_lower)

            # NOTE: For the next two operations the decorator is not used because the process needs to continue even
            #       on error. The report file documents all including Errors.
            # Get the bit depth
            try:
                resBitDepth = management.GetRasterProperties(in_raster=image.strFilePath_Moved,
                                                             property_type="VALUETYPE") # Returns a Results Object
                image.intBitDepth = resBitDepth
                strBitDepth = image.getBitDepthPlainLanguage()
            except ExecuteError:
                UtilityClassFunctionality.printAndLog(strGPErrorMsgBitDepthCheckFail.format(image.strFileName_lower, GetMessages(2)), UtilityClassFunctionality.WARNING_LEVEL)
                strBitDepth = UtilityClassFunctionality.ERROR_LEVEL
            except Exception as e:
                strBitDepth = UtilityClassFunctionality.ERROR_LEVEL
                UtilityClassFunctionality.printAndLog(e, UtilityClassFunctionality.WARNING_LEVEL)

            # Get the spatial reference
            try:
                spatrefProjectionName = Describe(image.strFilePath_Moved).spatialReference
                strProjectionName = str(spatrefProjectionName.name)
            except ExecuteError:
                UtilityClassFunctionality.printAndLog(strGPErrorMsgSpatialReferenceCheckFail.format(image.strFileName_lower, GetMessages(2)), UtilityClassFunctionality.WARNING_LEVEL)
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

            # Build tuple (HasTFW, BitDepth, Projection)
            tupFileData = (image.boolHasTFW, strBitDepth, strProjectionName, image.strPossibleUnits, image.strXYPixelSize)
            dictReportData[image.strFileName_lower] = tupFileData
        else:
            continue
except Exception as e:
    UtilityClassFunctionality.printAndLog(strErrorMsgBuildingReportFail.format(e), UtilityClassFunctionality.ERROR_LEVEL)

    # Create and Write the report file for use in excel etc.
strReportFileName = "{}{}".format(strDateTodayNoDashes, strReportFileEnding)
strReportFilePath = os.path.join(strReportFileLocation, strReportFileName)
try:
    with open(strReportFilePath,'w') as fReportFile:
        fReportFile.write("{},{},{},{},{},{}\n".format(strFileNameHeader, strHasTFWHeader, strBitDepthHeader, strProjectionHeader, strFeetVsMetersVsOtherHeader, strXYPixelSizeHeader))
        for key,value in dictReportData.iteritems():
            fReportFile.write("{},{},{},{},{},{}\n".format(key, value[0], value[1], value[2], value[3], value[4]))
except Exception as e:
    UtilityClassFunctionality.printAndLog(strErrorMsgOpeningWritingCSVFileFail.format(e), UtilityClassFunctionality.ERROR_LEVEL)
    exit()

UtilityClassFunctionality.printAndLog(strPSA_ProcessingCompleteSeeReport.format(strReportFilePath), UtilityClassFunctionality.INFO_LEVEL)
UtilityClassFunctionality.printAndLog(strPSA_ConsolidatedImageFilesLocation.format(strNewMasterImageCollectionFolderPath), UtilityClassFunctionality.INFO_LEVEL)

# Provide the user an opportunity to immediately move on to Step 2 after reviewing the report data.
try:
    strPromptForUserChoiceToContinueToStep2 = strPSA_MoveToStepTwoProcess
    strContinue = UtilityClassFunctionality.rawInputBasicChecks(strPromptForUserChoiceToContinueToStep2)
    if strContinue.lower() == strPSA_YESResponseToMoveToStepTwo:
        import TaxMapProcessing
        TaxMapProcessing
    else:
        UtilityClassFunctionality.printAndLog(strPSAProcessComplete, UtilityClassFunctionality.INFO_LEVEL)
except Exception as e:
    UtilityClassFunctionality.printAndLog(e, UtilityClassFunctionality.ERROR_LEVEL)
    exit()
"""
Evaluate .tif images for an accompanying .tfw file, the bit depth, and projection. Writes a report .csv with findings.

Completes step 1 of a 2 step process as of 20171109.
Step 1 is the pre-processing step used to check Tax Map Images from the MD Department of Planning
in order to avoid throwing errors later on in Step 2.
The script imports UtilityClass.py and ImageClass.py.
The script gathers two paths from the user using raw_input.
    path 1 is the directory for the image files
    path 2 is the directory where an output report csv file will be created
The script creates a csv file and populates it with data on the images.
Author: CJS
Date: 20171108
"""

#TODO: once script stabilizes refine imports to slim imported content
# Imports
from sys import exit
import os
import arcpy
import shutil
from datetime import date
from UtilityClass import UtilityClassFunctionality
import ImageClass

# VARIABLES
    # report file headers
strFileNameHeader = "Filename"
strHasTFWHeader = "HasTFW"
strBitDepthHeader = "BitDepth"
strProjectionHeader = "Projection"
    # Lists
lsImageObjects = []
lsAcceptableExtensionsForImageFilesOfInterest = ["tif","tfw","tif.xml"]
lsFileNamesTIF = []
lsFileNamesTFW = []
dictTFWCheck = {}

# INPUTS
    # Get the directory of the tif files to walk through
try:
    strPromptForImageDirectoryPath = "Paste the path for the directory of tiff files you want to process\n>"
    strInputFileDirectory = UtilityClassFunctionality.rawInputBasicChecks(strPromptForImageDirectoryPath)
    if not os.path.exists(strInputFileDirectory):
        exit()
    else:
        pass
except Exception as e:
    print "Image file directory appears to be invalid.\n{}".format(e)
    exit()

    # Get the path where a new folder will be created. The folder will hold all image files.
try:
    strPromptForNewImageDirectoryPath = "Paste the path where a new folder will be created and will hold a copy of all images for processing\n>"
    strNewFileDirectoryForAllImages = UtilityClassFunctionality.rawInputBasicChecks(strPromptForNewImageDirectoryPath)
    if not os.path.exists(strNewFileDirectoryForAllImages):
        exit()
    else:
        try:
            strNewFolderNameForAllImagesStorage = str(date.today()).replace("-", "") + "_AllTaxMapImages"
            strNewMasterImageCollectionFolderPath = os.path.join(strNewFileDirectoryForAllImages, strNewFolderNameForAllImagesStorage)
            os.mkdir(strNewMasterImageCollectionFolderPath)
            strReportFileLocation = strNewMasterImageCollectionFolderPath  # Report file will go in with images
        except Exception as e:
            print "Error creating new folder.\n{}".format(e)
            exit()
except Exception as e:
    print "The new directory appears to be invalid or already exists.\n{}".format(e)
    exit()

    # Step through the directory and all subdirectories. Create Image Objects for all files.
    # Write every image object filename to a list based on the file extension.
    # Notify the script user of the file extensions they are asking the script to examine and get a decision on proceed/exit
        # Basically a check for non TIF and TFW files such as zip files.
try:
    setOfFileExtensions = set()
    for (dirname, dirs, files) in os.walk(strInputFileDirectory):
        for eachFile in files:
            # Build image object, store in list, and set properties
            objImage = ImageClass.Image(dirname, str(eachFile))
            objImage.setFileName_lower()
            objImage.setFileExtension_lower()
            lsImageObjects.append(objImage)
            setOfFileExtensions.add(objImage.getFileExtension_lower())

            # Build list of TIF and TFW files for later use
            if objImage.getFileExtension_lower() == "tfw":
                lsFileNamesTFW.append(objImage.getFileName_lower())
            elif objImage.getFileExtension_lower() == "tif":
                lsFileNamesTIF.append(objImage.getFileName_lower())
            else:
                continue
    print "File extensions present in image datasets: {}".format(tuple(setOfFileExtensions))
    strPromptForUserConfirmation = "Proceed? (y/n)\n>"
    strUserCheck = UtilityClassFunctionality.rawInputBasicChecks(strPromptForUserConfirmation)
except Exception as e:
    print "Error walking directory and checking file extensions.\n{}".format(e)
    exit()

    # Check user entry to see if they are okay with the files about to be processed.
UtilityClassFunctionality.processUserEntry_YesNo(strUserCheck)
print "Processing...(moving files, checking for accompanying .tfw file, and retrieving bit depth and projection)"

#FUNCTIONALITY

    # Step through all Image Objects.
    #   Check that each .tif has a .tfw file. Write to dictionary with filename:(Zero for False, One for True)
    #   Check the bit depth of each .tif .
    #   Check the projection.
    #   Each record in report file will have "Filename,HasTFW,BitDepth,Projection"
    # Move all files to master location
try:
    for image in lsImageObjects:
        # Create string for new path, with a lowercase file name for standardizing moved image files, and check for existence to avoid error.
        strFullNewDestinationPathForFile_lowerfilename = os.path.join(strNewMasterImageCollectionFolderPath, image.getFileName_and_Extension().lower())
        if os.path.exists(strFullNewDestinationPathForFile_lowerfilename):
            print "File [{}] already exists in new location.".format(image.getFilePath_Original())
            exit()
        elif image.getFileExtension_lower() in lsAcceptableExtensionsForImageFilesOfInterest:
            image.setFilePath_Moved(strFullNewDestinationPathForFile_lowerfilename)
            # print "original: {}, destination: {}".format(image.getFilePath_Original(), image.getFilePath_Moved())
            shutil.move(image.getFilePath_Original(), image.getFilePath_Moved())
        else:
            continue
except Exception as e:
    print "Error while moving files.\n{}".format(e)
    exit()

    # Build the report data
        # Check the TIF to TFW relation
for tifFileName in lsFileNamesTIF:
    if tifFileName in lsFileNamesTFW:
        dictTFWCheck[tifFileName] = 1
    else:
        dictTFWCheck[tifFileName] = 0

        # Build the tuple of file data for the report file
dictReportData = {}
try:
    for image in lsImageObjects:
        strImageObjectExtension = image.getFileExtension_lower()
        if strImageObjectExtension == "tif":

            # Get the bit depth
            try:
                resBitDepth = arcpy.GetRasterProperties_management(in_raster=image.getFilePath_Moved(), property_type="VALUETYPE") # GetRasterProperties Returns a Results Object
                # UtilityClassFunctionality.examineResultObject(resBitDepth)
                strBitDepth = str(resBitDepth)
            except arcpy.ExecuteError:
                print "Geoprocessing error during image {} bit depth check: {}".format(image.getFileName_lower(),arcpy.GetMessages(2))
                strBitDepth = "Error"
            except Exception as e:
                strBitDepth = "Error"
                print e

            # Get the spatial reference
            try:
                spatrefProjectionName = arcpy.Describe(image.getFilePath_Moved()).spatialReference
                strProjectionName = str(spatrefProjectionName.name)
            except arcpy.ExecuteError:
                print "Geoprocessing error during image {} spatial reference check: {}".format(image.getFileName_lower(),arcpy.GetMessages(2))
                strProjectionName = "Error"
            except Exception as e:
                strProjectionName = "Error"
                print e

            # Build tuple (HasTFW, BitDepth, Projection)
            tupFileData = (dictTFWCheck.get(image.getFileName_lower()), strBitDepth, strProjectionName)
            dictReportData[image.getFileName_lower()] = tupFileData
        else:
            continue
except Exception as e:
    print "Error while building report data.\n{}".format(e)

#TODO: Determine if the below code can be refactored to use Image objects
    # Create and Write the report file for use in excel etc.
strReportFileName = str(date.today()).replace("-","") + "_TaxMapReportFile.csv"
strReportFilePath = os.path.join(strReportFileLocation, strReportFileName)
try:
    with open(strReportFilePath,'w') as fReportFile:
        fReportFile.write("{0},{1},{2},{3}\n".format(strFileNameHeader, strHasTFWHeader, strBitDepthHeader, strProjectionHeader))
        for key,value in dictReportData.iteritems():
            fReportFile.write("{0},{1},{2},{3}\n".format(key,value[0],value[1],value[2]))
except Exception as e:
    print "Error opening/writing to report file.\n{}".format(e)
    exit()

    # Provide the user the opportunity to trigger Step 2 now rather than starting it separate from this process.
print "Pre-Processing Complete. Please visit your report and review the contents.\n\n\tREPORT LOCATION > {}\n".format(strReportFilePath)

# Provide the user an opportunity to immediately move on to Step 2 after reviewing the report data.
try:
    strPromptForUserChoiceToContinueToStep2 = "If the images files looks satisfactory, based on the report findings, type a 'y' to run Step 2 now. Type 'n' to stop.\n>"
    strContinue = UtilityClassFunctionality.rawInputBasicChecks(strPromptForUserChoiceToContinueToStep2)
    if strContinue == "y":
        import TaxMapProcessing
        TaxMapProcessing
except Exception as e:
    print e
    exit()


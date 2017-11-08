####################
#
#
#
#
#
#
####################
#TODO: once script stabilizes refine imports to slim imported content
# Imports
from sys import exit
import os
import arcpy
import shutil
from datetime import date
import UtilityClass
import ImageClass

# VARIABLES
    # report file headers
strFileNameHeader = "Filename"
strHasTFWHeader = "HasTFW"
strBitDepthHeader = "BitDepth"
strProjectionHeader = "Projection"
    # utility class instance
classUtilClass = UtilityClass.UtilityClassFunctionality()
    # Lists
lsImageObjects = []
lsAcceptableExtensionsForImageFilesOfInterest = ["tif","tfw","tif.xml"]
lsFileNamesTIF = []
lsFileNamesTFW = []
dictTFWCheck = {}


# INPUTS
    # Get the directory of the tif files to walk through
try:
    strInputFileDirectory = raw_input("Paste the path for the directory of tiff files you want to process\n>")
    if not os.path.exists(strInputFileDirectory):
        exit()
    else:
        pass
except:
    print "Image file directory appears to be invalid"
    exit()

    # Get the path where a new folder will be created. The folder will hold all image files.
try:
    strNewFileDirectoryForAllImages = raw_input("Paste the path where a new folder will be created and will hold a copy of all images for processing\n>")
    if not os.path.exists(strNewFileDirectoryForAllImages):
        exit()
    else:
        try:
            strNewFolderNameForAllImagesStorage = str(date.today()).replace("-", "") + "_AllTaxMapImages"
            strNewMasterImageCollectionFolderPath = os.path.join(strNewFileDirectoryForAllImages, strNewFolderNameForAllImagesStorage)
            os.mkdir(strNewMasterImageCollectionFolderPath)
            strReportFileLocation = strNewMasterImageCollectionFolderPath  # Report file will go in with images
        except:
            print "Error creating new folder. Exiting..."
            exit()
except:
    print "The new directory appears to be invalid or already exists. Exiting."
    exit()

    # Notify the script user of the file extensions they are asking the script to examine and get a decision on proceed/exit
        # Basically a check for non TIF and TFW files.
try:
    setOfFileExtensions = set()
    for (dirname, dirs, files) in os.walk(strInputFileDirectory):
        for file in files:
            # Build image object, store in list, and set properties
            objImage = ImageClass.Image(dirname, str(file))
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
    strUserCheck = raw_input("Care to proceed? (y/n)\n")
except:
    print "Error walking directory and checking file extensions."
    exit()

    # Check user entry to see if they are okay with the files about to be processed.
classUtilClass.processUserEntry_YesNo(strUserCheck)
print "Processing..."

#FUNCTIONALITY

    # Step through the directory and all subfolders.
    #   Write every filename to a list based on the file extension. (Completed above)
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
except:
    print "Error while moving file."
    exit()

    # Build the report data
        # Check the TIF to TFW relation
for tifFileName in lsFileNamesTIF:
    if tifFileName in lsFileNamesTFW:
        dictTFWCheck[tifFileName] = 1
    else:
        dictTFWCheck[tifFileName] = 0
# print "lsFileNamesTIF\n {}".format(lsFileNamesTIF)
# print "lsFileNamesTFW\n {}".format(lsFileNamesTFW)
# print "dictTFWCheck\n {}".format(dictTFWCheck)

        # Build the tuple of file data for the report file
dictReportData = {}
try:
    for image in lsImageObjects:
        strImageObjectExtension = image.getFileExtension_lower()
        if strImageObjectExtension == "tif":

            # Get the bit depth
            try:
                resBitDepth = arcpy.GetRasterProperties_management(in_raster=image.getFilePath_Moved(), property_type="VALUETYPE") # GetRasterProperties Returns a Results Object
                # classUtilClass.examineResultObject(resBitDepth)
                strBitDepth = str(resBitDepth)
            except:
                strBitDepth = "Error"

            # Get the spatial reference
            try:
                spatrefProjectionName = arcpy.Describe(image.getFilePath_Moved()).spatialReference
                strProjectionName = str(spatrefProjectionName.name)
            except:
                strProjectionName = "Error"

            # Build tuple (HasTFW, BitDepth, Projection)
            # print dictTFWCheck.get(tupFileNameParts[0].lower())
            tupFileData = (dictTFWCheck.get(image.getFileName_lower()), strBitDepth, strProjectionName)
            dictReportData[image.getFileName_lower()] = tupFileData
        else:
            continue
except:
    print "Error while building report data"

#TODO: Determine if the below code can be refactored to use Image objects
    # Create and Write the report file for use in excel etc.
strReportFileName = str(date.today()).replace("-","") + "_TaxMapReportFile.csv"
strReportFilePath = os.path.join(strReportFileLocation, strReportFileName)
try:
    with open(strReportFilePath,'w') as fReportFile:
        fReportFile.write("{0},{1},{2},{3}\n".format(strFileNameHeader, strHasTFWHeader, strBitDepthHeader, strProjectionHeader))
        for key,value in dictReportData.iteritems():
            fReportFile.write("{0},{1},{2},{3}\n".format(key,value[0],value[1],value[2]))
except:
    print "Error opening/writing to report file"
    exit()

print "Preprocessing Complete. Visit your report. {}".format(strReportFilePath)

# DELETIONS
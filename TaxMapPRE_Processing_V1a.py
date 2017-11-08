# Imports
import sys, os
import arcpy
import shutil
from datetime import date
import UtilityClass

# VARIABLES
    # report file headers
strFileNameHeader = "Filename"
strHasTFWHeader = "HasTFW"
strBitDepthHeader = "BitDepth"
strProjectionHeader = "Projection"
    # tuples of acceptable file extensions, should there be variations
tupAcceptableFileExtensionsTIF = ("tif","tiff")
tupAcceptableFileExtensionsTWF = ("twf")
    # environments
arcpy.env.workspace = r"E:\TaxMapsProject\Testing\TestImages"
arcpy.env.overwriteOutput = True
    # utility class instance
classUtilClass = UtilityClass.UtilityClassFunctionality()
    # Lists
lsFileNamesTIF = []
lsFileNamesTFW = []
dictTFWCheck = {}

# INPUTS
    # Get the directory of the tif files to walk through
try:
    strInputFileDirectory = raw_input("Paste the path for the directory of tiff files you want to process\n")
    if not os.path.exists(strInputFileDirectory):
        sys.exit()
    else:
        pass
except:
    print "Image file directory appears to be invalid"
    sys.exit()

    # Get the path where a new folder will be created. The folder will hold all image files.
try:
    strNewFileDirectoryForAllImages = raw_input("Paste the path where a new folder will be created and will hold a copy of all images for processing\n")
    if not os.path.exists(strNewFileDirectoryForAllImages):
        sys.exit()
    else:
        try:
            strNewFolderNameForAllImagesStorage = str(date.today()).replace("-", "") + "_AllTaxMapImages"
            strNewMasterImageCollectionFolderPath = os.path.join(strNewFileDirectoryForAllImages, strNewFolderNameForAllImagesStorage)
            os.mkdir(strNewMasterImageCollectionFolderPath)
            strReportFileLocation = strNewMasterImageCollectionFolderPath  # Report file will go in with images
        except:
            print "Error creating new folder. Exiting..."
            sys.exit()
except:
    print "The new directory appears to be invalid or already exists. Exiting."
    sys.exit()

    # Notify the script user of the file extensions they are asking the script to examine and get a decision on proceed/exit
    #   Basically a check for non TIF and TFW files.
try:
    #TODO: simplify this section with use of set(put list here) and list comprehension for '.tfw' and '.tif' files
    setOfFileExtensions = set()
    for (dirname, dirs, files) in os.walk(strInputFileDirectory):
        for file in files:
            tupFileNameParts = file.split(".")
            # print tupFileNameParts
            setOfFileExtensions.add(tupFileNameParts[1].lower())

            # Build list of TIF and TFW files for later use
            if "tfw" in tupFileNameParts[1].lower():
                lsFileNamesTFW.append(str(tupFileNameParts[0].lower()))
            elif "tif" in tupFileNameParts[1].lower():
                lsFileNamesTIF.append(str(tupFileNameParts[0].lower()))
            else:
                continue
    print "File extensions present in image datasets: {}".format(tuple(setOfFileExtensions))
    strUserCheck = raw_input("Care to proceed? (y/n)\n")
    print "Processing..."
except:
    print "Error walking directory and checking file extensions."
    sys.exit()

    # Check user entry to see if they are okay with the files about to be processed.
classUtilClass.processUserEntry_YesNo(strUserCheck)

#FUNCTIONALITY

    # Step through the directory and all subfolders.
    #   Write every filename to a list based on the file extension. (Completed above)
    #   Check that each .tif has a .tfw file. Write to dictionary with filename:(Zero for False, One for True)
    #   Check the bit depth of each .tif .
    #   Check the projection.
    #   Each record in report file will have "Filename,HasTFW,BitDepth,Projection"

    # Move all files to master location
    #TODO: Determine why this doesn't now work on folders of images within the directory of choice
try:
    for (dirname, dirs, files) in os.walk(strInputFileDirectory):
        for file in files:
            file = file.lower()
            strFileDestination = os.path.join(strNewMasterImageCollectionFolderPath, file)
            if os.path.exists(strFileDestination):
                break
            elif file.endswith(".tfw") or file.endswith(".tif") or file.endswith("tif.xml"):
                strFilePath = os.path.join(strInputFileDirectory, file)
                # print "strFileDestination: {}".format(strFileDestination)
                #TODO: Account for xml files that are with the images. The xml file contains the projection information. For instance alle001.tif will have alle001.tfw and alle001.tif.xml
                shutil.move(strFilePath, strFileDestination)
            else:
                continue
except:
    print "Error copying file: {}".format(file)
    sys.exit()

    # Build the report data
        # Check the TIF to TFW relation
for tifFileName in lsFileNamesTIF:
    if tifFileName in lsFileNamesTFW:
        dictTFWCheck[tifFileName] = 1
    else:
        dictTFWCheck[tifFileName] = 0
# print "dictTFWCheck\n {}".format(dictTFWCheck)

        # Build the tuple of file data for the report file
dictReportData = {}
try:
    for (dirname, dirs, files) in os.walk(strNewMasterImageCollectionFolderPath):
        # print "dirname: {}".format(dirname)
        for file in files:
            tupFileNameParts = file.split(".")
            # print "file: {}, filename: {}".format(file,tupFileNameParts[0])
            if tupFileNameParts[-1].lower() == "tif":

                # Get the bit depth
                try:
                    resBitDepth = arcpy.GetRasterProperties_management(in_raster=str(file), property_type="VALUETYPE") # GetRasterProperties Returns a Results Object
                    # classUtilClass.examineResultObject(resBitDepth)
                    strBitDepth = str(resBitDepth)
                except:
                    strBitDepth = "Error"

                # Get the spatial reference
                try:
                    spatrefProjectionName = arcpy.Describe(file).spatialReference
                    strProjectionName = str(spatrefProjectionName.name)
                except:
                    strProjectionName = "Error"

                # print tupFileNameParts[0].lower()
                # print strBitDepth
                # print strProjectionName
                # Build tuple (HasTFW, BitDepth, Projection)
                # print dictTFWCheck.get(tupFileNameParts[0].lower())
                tupFileData = (dictTFWCheck.get(tupFileNameParts[0].lower()), strBitDepth, strProjectionName)
                # print tupFileData, "\n"
                dictReportData[tupFileNameParts[0]] = tupFileData
            else:
                continue
except:
    print "Error while building report data"
# print dictReportData

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
    sys.exit()

print "Preprocessing Complete. Visit your report. {}".format(strReportFilePath)

# DELETIONS
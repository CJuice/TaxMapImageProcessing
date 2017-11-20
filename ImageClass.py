import os
class Image(object):
    """
    Object template for each part of the .tif image files (tif, tfw, tif.xml, etc)
    """
    xRangeWKID26985 = (185218.488100,570274.874800)
    yRangeWKID26985 = (24686.339700,230946.080000)
    xRangeWKID2248 = (607670.989729,1870976.818427)
    yRangeWKID2248 = (80991.766092,757695.597392)

    def __init__(self, strFileDirname, strNameCombo, strNewConsolidatedImageFolderPath):
        """
        Instantiate an image object.

        :param strFileDirname: Directory path
        :param strNameCombo: File name and extension
        """
        self.strFileDirectoryPath = strFileDirname
        self.strFileName_and_Extension = strNameCombo
        self.strConsolidatedImageFileDirectoryPath = strNewConsolidatedImageFolderPath
        self.strFilePath_Original = os.path.join(strFileDirname, strNameCombo)
        self.strFilePath_Moved = None
        self.strFileName_lower = None
        self.strFileExtension_lower = None
        self.boolHasTFW = False
        self.intBitDepth = -99
        self.strProjection = None
        self.floatTFW_XCoord = 0.0
        self.floatTFW_YCoord = 0.0
        self.strPossibleUnits = None
        self.lsTFWContents = []
        self.strXYPixelSize = None

    # METHODS
    def storeTFWContentsInList(self):
        tfwFileNameAndExtension = "{}.{}".format(self.strFileName_lower, "tfw")
        strTFWPath = os.path.join(self.strConsolidatedImageFileDirectoryPath, tfwFileNameAndExtension)
        with open(strTFWPath) as fOpen:
            for line in fOpen:
                line = line.rstrip()
                self.lsTFWContents.append(line)

    def detectPossibleProjectionUnitsFromTFWList(self):
        (x,y) = (self.floatTFW_XCoord,self.floatTFW_YCoord)
        if (x > Image.xRangeWKID26985[0] and x < Image.xRangeWKID26985[1]) and (y > Image.yRangeWKID26985[0] and y < Image.yRangeWKID26985[1]):
            self.strPossibleUnits = "METERS"
        elif (x > Image.xRangeWKID2248[0] and x < Image.xRangeWKID2248[1]) and (y > Image.yRangeWKID2248[0] and y < Image.yRangeWKID2248[1]):
            self.strPossibleUnits = "FEET"
        else:
            self.strPossibleUnits = "OTHER"

    # SETTERS
    def setFileName_lower(self):
        """
        Set the file name in lowercase.

        :return:
        """
        self.strFileName_lower = (self.strFileName_and_Extension.split(".")[0]).lower()

    def setFileExtension_lower(self):
        """
        Set the file extension in lower case

        :return:
        """
        lsFileParts = (self.strFileName_and_Extension.lower()).split(".")
        if ("tif" and "xml" in lsFileParts) and (len(lsFileParts) == 3):
            self.strFileExtension_lower = "{}.{}".format(lsFileParts[-2].lower(),lsFileParts[-1].lower())
        else:
            self.strFileExtension_lower = lsFileParts[-1].lower()

    def setBitDepth(self, resultObject):
        """
        Set the Bit Depth of the .tif image

        :param resultObject: Result object from GetRasterProperties tool
        :return:
        """
        self.intBitDepth = int(str(resultObject))


    def setFilePath_Moved(self, strNewMasterImageCollectionFolderPath):
        """
        Set the file path of the relocated image.

        :param strNewMasterImageCollectionFolderPath:
        :return:
        """
        # self.strDestinationFilePathDirectory_Moved = os.path.join(strNewMasterImageCollectionFolderPath)
        self.strFilePath_Moved = strNewMasterImageCollectionFolderPath

    def setHasTFW(self, booleanValue):
        self.boolHasTFW = booleanValue

    def setXYCoordinatesUpperLeftCornerOfImageFromTFWList(self):
        self.floatTFW_XCoord = float(self.lsTFWContents[4])
        self.floatTFW_YCoord = float(self.lsTFWContents[5])

    def setXYPixelSizeFromTFWList(self):
        if abs(float(self.lsTFWContents[0])) == abs(float(self.lsTFWContents[3])):
            self.strXYPixelSize = "{}".format(abs(float(self.lsTFWContents[0])))
        else:
            self.strXYPixelSize = "{} \ {}".format(self.lsTFWContents[0],self.lsTFWContents[3])

    # GETTERS
    def getFilePath_Original(self):
        """
        Get the original file path from before relocation of the image file.

        :return: String path
        """
        return self.strFilePath_Original

    def getFileName_lower(self):
        """
        Get the lowercase file name.

        :return: String
        """
        return self.strFileName_lower

    def getFileExtension_lower(self):
        """
        Get the lowercase file extension.

        :return: String
        """
        return self.strFileExtension_lower

    def getFileName_and_Extension(self):
        """
        Get the original filename.extensions as read during the os.walk through the directory.

        :return: String
        """
        return self.strFileName_and_Extension

    def getFilePath_Moved(self):
        """
        Get the path of the relocated image file.

        :return: String path
        """
        return self.strFilePath_Moved

    def getBitDepthPlainLanguage(self):
        """

        :return:
        """
        dictBitDepthPlainLanguage = {0: "1-bit", 1: "2-bit", 2: "4-bit", 3: "8-bit unsigned integer",
                                     4: "8-bit signed integer", 5: "16-bit unsigned integer",
                                     6: "16-bit signed integer", 7: "32-bit unsigned integer",
                                     8: "32-bit signed integer", 9: "32-bit floating point",
                                     10: "64-bit double precision", 11: "8-bit complex", 12: "16-bit complex",
                                     13: "32-bit complex", 14: "64-bit complex"}
        return dictBitDepthPlainLanguage[self.intBitDepth]

    def getHasTFW(self):
        return self.boolHasTFW

    def getPossibleUnits(self):
        return self.strPossibleUnits

    def getPixelDimensions(self):
        return self.strXYPixelSize
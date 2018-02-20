import os, re
class Image(object):
    """
    Object template for each part of the .tif image files (tif, tfw, tif.xml, etc)
    """
    __X_RANGE_WKID26985 = (185218.488100, 570274.874800)
    __Y_RANGE_WKID26985 = (24686.339700, 230946.080000)
    __X_RANGE_WKID2248 = (607670.989729, 1870976.818427)
    __Y_RANGE_WKID2248 = (80991.766092, 757695.597392)

    def __init__(self, strFileDirname, strNameCombo, strNewConsolidatedImageFolderPath):
        """
        Instantiate an image object.

        :param strFileDirname: Directory path
        :param strNameCombo: File name and extension
        :param strNewConsolidatedImageFolderPath: path to consolidated images for processing
        """
        self.strFileDirectoryPath = strFileDirname
        self.strFileName_and_Extension = strNameCombo
        self.strConsolidatedImageFileDirectoryPath = strNewConsolidatedImageFolderPath
        self.strFilePath_Original = os.path.join(strFileDirname, strNameCombo)
        self.strCleanedFileName_and_Extension = None
        self.strCleanFileName = None
        self.strFilePath_Moved = None
        self.strFileName_lower = None
        self.strFileExtension_lower = None
        self.boolHasTFW = False
        self.intBitDepth = -99
        self.strProjection = None
        self.__floatTFW_XCoord = 0.0
        self.__floatTFW_YCoord = 0.0
        self.strPossibleUnits = None
        self.__lsTFWContents = []
        self.strXYPixelSize = None

    # METHODS
    def storeTFWContentsInList(self):
        """
        Open a .tfw file, read the contents, store in a list for later access.

        :return:
        """
        # tfwFileNameAndExtension = "{}.{}".format(self.strFileName_lower, "tfw")
        tfwFileNameAndExtension = "{}.{}".format(self.strCleanFileName, "tfw")

        strTFWPath = os.path.join(self.strConsolidatedImageFileDirectoryPath, tfwFileNameAndExtension)
        with open(strTFWPath) as fOpen:
            for line in fOpen:
                line = line.rstrip()
                if len(line) > 0:
                    self.__lsTFWContents.append(line)

    def setXYCoordinatesUpperLeftCornerOfImageFromTFWList(self):
        """
        Set the x and y coordinate values.

        :return:
        """
        self.__floatTFW_XCoord = float(self.__lsTFWContents[4])
        self.__floatTFW_YCoord = float(self.__lsTFWContents[5])

    def detectPossibleProjectionUnitsFromTFWList(self):
        """
        Determine the units of the image dimensions and location through the range of values for the x and y coordinates.

        :return:
        """
        (x,y) = (self.__floatTFW_XCoord,self.__floatTFW_YCoord)
        if (x > Image.__X_RANGE_WKID26985[0] and x < Image.__X_RANGE_WKID26985[1]) and (y > Image.__Y_RANGE_WKID26985[0] and y < Image.__Y_RANGE_WKID26985[1]):
            self.strPossibleUnits = "METERS"
        elif (x > Image.__X_RANGE_WKID2248[0] and x < Image.__X_RANGE_WKID2248[1]) and (y > Image.__Y_RANGE_WKID2248[0] and y < Image.__Y_RANGE_WKID2248[1]):
            self.strPossibleUnits = "FEET"
        else:
            self.strPossibleUnits = "OTHER"

    def getBitDepthPlainLanguage(self):
        """
        Get the bit depth plain language description.

        :return: String
        """
        dictBitDepthPlainLanguage = {0: "1-bit", 1: "2-bit", 2: "4-bit", 3: "8-bit unsigned integer",
                                     4: "8-bit signed integer", 5: "16-bit unsigned integer",
                                     6: "16-bit signed integer", 7: "32-bit unsigned integer",
                                     8: "32-bit signed integer", 9: "32-bit floating point",
                                     10: "64-bit double precision", 11: "8-bit complex", 12: "16-bit complex",
                                     13: "32-bit complex", 14: "64-bit complex"}
        return dictBitDepthPlainLanguage[self.intBitDepth]

    def setXYPixelSizeFromTFWList(self):
        """
        Set the string representation of the x and y pixel dimensions.

        For writing to the report file.
        :return:
        """
        if abs(float(self.__lsTFWContents[0])) == abs(float(self.__lsTFWContents[3])):
            self.strXYPixelSize = "{}".format(abs(float(self.__lsTFWContents[0])))
        else:
            self.strXYPixelSize = "{} \ {}".format(self.__lsTFWContents[0], self.__lsTFWContents[3])

        # GETTERS/SETTERS
    @property
    def strCleanedFileName_and_Extension(self):
        return self.__strCleanedFileName_and_Extension

    @strCleanedFileName_and_Extension.setter
    def strCleanedFileName_and_Extension(self, val=None):
        """
        Clean the file name and extension of illegal characters.

        Must be alpha, numeric, period, or underscore
        :param val:
        :return:
        """
        cleaned = re.sub(r'[^a-zA-Z0-9_.]', '_', self.strFileName_and_Extension)
        self.__strCleanedFileName_and_Extension = cleaned
        self.strFileName_lower = cleaned
        return

    @property
    def strCleanFileName(self):
        return self.__strCleanFileName

    @strCleanFileName.setter
    def strCleanFileName(self, val=None):
        """
        Create a clean file name without extension
        :param val:
        :return:
        """
        self.__strCleanFileName = (self.strCleanedFileName_and_Extension.split("."))[0]

    @property
    def strFileName_lower(self):
        return self.__strFileName_lower

    @strFileName_lower.setter
    def strFileName_lower(self, val=None):
        """
        Calculate & set the file name in lowercase
        :param val:
        :return:
        """
        self.__strFileName_lower = (self.strFileName_and_Extension.split(".")[0]).lower()
        return

    @property
    def strFileExtension_lower(self):
        return self.__strFileExtension_lower

    @strFileExtension_lower.setter
    def strFileExtension_lower(self, val=None):
        """
        Set the file extension in lower case

        :return:
        """

        lsFileParts = (self.strFileName_and_Extension.lower()).split(".")
        if ("tif" and "xml" in lsFileParts) and (len(lsFileParts) == 3):
            self.__strFileExtension_lower = "{}.{}".format(lsFileParts[-2].lower(), lsFileParts[-1].lower())
        else:
            self.__strFileExtension_lower = lsFileParts[-1].lower()
        return

    @property
    def intBitDepth(self):
        return self.__intBitDepth

    @intBitDepth.setter
    def intBitDepth(self, val):
        """
        Set the Bit Depth of the .tif image

        :param resultObject: Result object from GetRasterProperties tool
        :return:
        """
        # self.__intBitDepth = int(str(val))
        self.__intBitDepth = int(str(val))
        return
import os
class Image(object):
    """
    Object template for each part of the .tif image files (tif, tfw, tif.xml, etc)
    """

    def __init__(self, strFileDirname, strNameCombo):
        """
        Instantiate an image object.

        :param strFileDirname: Directory path
        :param strNameCombo: File name and extension
        """
        self.strFileDirectoryPath = strFileDirname
        self.strFileName_and_Extension = strNameCombo
        self.strFilePath_Original = os.path.join(strFileDirname, strNameCombo)
        self.strFileName_lower = None
        self.strFileExtension_lower = None
        self.strHasTFW = False
        self.intBitDepth = -99
        self.strProjection = None
        self.strFilePath_Moved = None

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
        self.strFilePath_Moved = os.path.join(strNewMasterImageCollectionFolderPath)

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
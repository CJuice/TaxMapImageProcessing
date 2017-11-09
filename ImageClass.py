import os
class Image(object):
    """
    Object template for each part of the .tif image files (tif, tfw, tif.xml, etc)
    """

    def __init__(self, strFileDirname, strNameCombo):
        """
        Instantiate an image object.

        :param strFileDirname:
        :param strNameCombo:
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

    def setBitDepth(self):
        """
        Set the Bit Depth of the .tif image

        :return:
        """

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
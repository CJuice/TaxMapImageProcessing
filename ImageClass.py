import os
class Image(object):
    """Object template for each part of our image files (tif, tfw, tif.xml, etc)"""

    def __init__(self, strFileDirname, strNameCombo):
        """Initialize the image object"""
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
        """"""
        self.strFileName_lower = (self.strFileName_and_Extension.split(".")[0]).lower()

    def setFileExtension_lower(self):
        """"""
        lsFileParts = (self.strFileName_and_Extension.lower()).split(".")
        if ("tif" and "xml" in lsFileParts) and (len(lsFileParts) == 3):
            self.strFileExtension_lower = "{}.{}".format(lsFileParts[-2].lower(),lsFileParts[-1].lower())
        else:
            self.strFileExtension_lower = lsFileParts[-1].lower()

    def setBitDepth(self):
        """"""
        pass

    def setFilePath_Moved(self, strNewMasterImageCollectionFolderPath):
        """"""
        self.strFilePath_Moved = os.path.join(strNewMasterImageCollectionFolderPath)

    # GETTERS
    def getFilePath_Original(self):
        """"""
        return self.strFilePath_Original

    def getFileName_lower(self):
        """"""
        return self.strFileName_lower

    def getFileExtension_lower(self):
        """"""
        return self.strFileExtension_lower

    def getFileName_and_Extension(self):
        """"""
        return self.strFileName_and_Extension

    def getFilePath_Moved(self):
        """"""
        return self.strFilePath_Moved
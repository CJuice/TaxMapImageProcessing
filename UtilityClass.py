class UtilityClassFunctionality(object):
    """
    Utility methods for use in scripts.
    """

    def __init__(self):
        """
        Instantiate UtilityClassFunctionality object

        As of 20171109 all methods were static.
        """
        pass

    @staticmethod
    def processUserEntry_YesNo(strUserEntry):
        """
        Evaluate the users response to a raw_input for yes or no.

        Static method in UtilityClass
        :param strUserEntry:
        :return:
        """

        import sys
        if strUserEntry.lower() == "y":
            pass
        else:
            sys.exit()

    @staticmethod
    def examineResultObject(resultObjectFromESRIProcess):
        """
        Examine the result object generated from an ESRI process.

        :param resultObjectFromESRIProcess:
        :return:
        """

        lenResult = len(resultObjectFromESRIProcess)
        print "len: {}".format(lenResult)
        for i in range(0,lenResult):
            strTemp = str(resultObjectFromESRIProcess[i])
            print "\t{}".format(strTemp)
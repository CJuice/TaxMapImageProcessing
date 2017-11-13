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
    def rawInputBasicChecks(strRawInputPromptSentence):
        """"""
        strUserInput = None
        while True:
            strUserInput = raw_input(strRawInputPromptSentence)
            if strUserInput == None or len(strUserInput) == 0:
                pass
            else:
                break
        return strUserInput

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

#TODO: Customize the printed error message for the tool being passed through.
    @staticmethod
    def captureAndPrintGeoprocessingErrors(func):
        from arcpy import ExecuteError, GetMessages

        def f(*args, **kwargs):
            try:
                rv = func(*args, **kwargs)
            except ExecuteError:
                print "Error creating Raster Catalog.\n{}".format(GetMessages(2))
                return exit()
            except Exception as e:
                print e
                return exit()
            return rv
        return f
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
        """
        Prompt user for input and check for empty entry.

        Static method in UtilityClass
        :param strRawInputPromptSentence: The prompting language to help user
        :return: String
        """
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
        :param strUserEntry: Users entry
        :return: No return, or return exit on fail
        """
        if strUserEntry.lower() == "y":
            pass
        else:
            return exit()

    @staticmethod
    def examineResultObject(resultObjectFromESRIProcess):
        """
        Examine the result object generated from an ESRI process.

        Static method in UtilityClass
        :param resultObjectFromESRIProcess: result object from geoprocessing process
        :return: No return
        """
        lenResult = len(resultObjectFromESRIProcess)
        print "len: {}".format(lenResult)
        for i in range(0,lenResult):
            strTemp = str(resultObjectFromESRIProcess[i])
            print "\t{}".format(strTemp)

    @staticmethod
    def captureAndPrintGeoprocessingErrors(func):
        """
        Wrap a function with try and except. Decorator.

        :param func: The ESRI geoprocessing function object
        :return: The resulting value from the tool on successful run, or exit on fail.
        """
        import logging
        from arcpy import ExecuteError, GetMessages
        def f(*args, **kwargs):
            try:
                resultValue = func(*args, **kwargs)
            except ExecuteError:
                print "Geoprocessing Error.\n{}".format(GetMessages(2))
                logging.error("UtilityClass.captureAndPrintGeoprocessingErrors: Geoprocessing Error.\n{}".format(GetMessages(2)))
                return exit()
            except Exception as e:
                print e
                logging.error("UtilityClass.captureAndPrintGeoprocessingErrors: {}".format(e))
                return exit()
            return resultValue
        return f

    @staticmethod
    def checkPathExists(strPath):
        """
        Check for path existence.

        :param strPath: The path of interest
        :return: No return, or exit on fail
        """
        import os.path
        if os.path.exists(strPath):
            return
        else:
            print "Path does not exist."
            return exit()

    @staticmethod
    def printAndLog(strMessage, strLogLevel):
        """

        :param strMessage:
        :param strLogLevel:
        :return:
        """
        import logging
        strInfo = "info"
        strWarning = "warning"
        strError = "error"
        strMessage = strMessage.strip("\n")
        if strLogLevel is strInfo:
            logging.info(strMessage)
        elif strLogLevel is strWarning:
            logging.warning(strMessage)
        elif strLogLevel is strError:
            logging.warning(strMessage)
        print(strMessage)
        return
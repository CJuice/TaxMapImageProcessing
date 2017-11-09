class UtilityClassFunctionality(object):
    """"""

    def __init__(self):
        pass

    @staticmethod
    def processUserEntry_YesNo(self,strUserEntry):
        """Enter Description"""
        import sys
        if strUserEntry.lower() == "y":
            pass
        else:
            sys.exit()

    @staticmethod
    def examineResultObject(self, resultObjectFromESRIProcess):
        """Enter Description"""
        lenResult = len(resultObjectFromESRIProcess)
        print "len: {}".format(lenResult)
        for i in range(0,lenResult):
            strTemp = str(resultObjectFromESRIProcess[i])
            print "\t{}".format(strTemp)
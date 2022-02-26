from ExceptionPolicy import *

#Class to handle exceptions within the system and off load them to a log file
class ExceptionManager(object):
    def __init__(self, logFile=None):
        if logFile is None:
            from Classes.ExtensionMethods import ExtensionMethods
            logFile = ExtensionMethods.LoadData("Audit")
        self.__logFile = logFile

    def handleException(self, ex, policy=ExceptionPolicy._policyLogAndCotinue):
        strEx = str(ex)
        print(strEx) #Print Exception
        self.__writeToLogFile(strEx)
        if policy == ExceptionPolicy._policyLogAndCotinue:
            pass
        
    def __writeToLogFile(self, msg):
        with open(self.__logFile, "a") as exFile:
            exFile.writelines(msg)
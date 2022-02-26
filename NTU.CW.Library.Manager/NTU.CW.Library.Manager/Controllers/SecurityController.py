from GUIInterface.SecurityGUI import *
from Classes.ExtensionMethods import ExtensionMethods 
from Classes.CatalogueProvider import CatalogueProvider
from Modules.Security.AuthorizationManager import AuthorizationManager
from Modules.Exception.ExceptionManager import ExceptionManager
from Models.Security.User import User

#Controller Class which holds the Views and Logic for Security
class SecurityController(object):
    def __init__(self):
        self.__GUI = SecurityGUI(self)
        self.__exceptionManager = ExceptionManager()
        
    #Fowards on the window to the GUI method loginRegisterMenu View
    def loginRegisterMenu(self, window):
        self.__GUI.loginRegisterMenu(window)
        
    #Fowards on the window to the GUI method LoginMenuRedirect View
    def LoginMenuRedirect(self, window):
        self.__GUI.loginMenu(window)
        
    #Fowards on the window to the GUI method loginRegisterMenu View
    def Logout(self, window):
        self.__GUI.loginRegisterMenu(window)
        
    #Fowards on the window to the GUI method Profile View
    def Profile(self, window):
        self.__GUI.profile(window)
        
    #Fowards on the window to the GUI method Members View
    def Members(self, window):
        self.__GUI.members(window)

        
    #Logons on the user with the Username and password (md5) checked, saves the instance of the user to memeory
    def Login(self, username, password):
        resultBool = False
        try:
            _user = None
            if len(username) > 0 and len(password) > 0:
                resultBool, _user = AuthorizationManager.CheckUserCred(username, password)
                if resultBool:
                    AuthorizationManager.userInstance = _user
        except Exception as ex:
            self.__exceptionManager.handleException(ex)
        return resultBool

    def ListUsers(self):
        users = list()
        userCSV = ExtensionMethods.LoadData("SecurityUsers")
        for _userRow in userCSV:
            if len(_userRow["_Id"]) > 0:
                _user = User(int(_userRow["_Id"]), int(_userRow["_Type"]), _userRow["Username"], _userRow["FirstName"], _userRow["LastName"])
                users.append(_user)
        return users
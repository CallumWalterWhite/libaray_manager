from Models.Security.SecurityType import SecurityType

#Class User holds information of users that repersents the type of Member and Librarian
class User(object):
    def __init__(self, _id, securityType, username, firstName, lastName):
        self.__id = _id
        self._type = int(securityType)
        self.__username = username
        self.__firstName = firstName
        self.__lastName = lastName
        self.__resetPasswordBool = False
        self.history = list()
        
    def GetUserId(self):
        return int(self.__id)

    def GetUserName(self):
        return self.__username
    def GetFirstName(self):
        return self.__firstName
    def GetLastName(self):
        return self.__lastName
    def GetTypeName(self):
        return SecurityType(self._type).name
    def GetDefaultPassword(self):
        return self.__defaultPassword
    def GetResetPassword(self):
        if self.__resetPasswordBool:
            return self.__resetPassword
        else:
            return None
    def SetUserName(self, _username):
        self.__username = _username
    def SetFirstName(self, _firstName):
        self.__firstName = _firstName
    def SetLastName(self, _lastName):
        self.__lastName = _lastName
    def SetDefaultPassword(self, _pw):
        self.__defaultPassword = _pw
    def SetResetPassword(self, pw):
        self.__resetPasswordBool = True
        self.__resetPassword = pw;

    #Saves this instance of User to the SecurityUser CSV
    def SaveDetails(self):
        from Modules.Security.AuthorizationManager import AuthorizationManager
        return AuthorizationManager.SaveUserDetail(self)

    def GetObject(self):
        return {
                "_Id": self.__id
                ,   "_Type": self._type
                ,   "Username": self.__username
                ,   "FirstName": self.__firstName
                ,   "LastName": self.__lastName
            }


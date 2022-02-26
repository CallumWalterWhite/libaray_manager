from Models.Security.SecurityType import SecurityType
from Classes.ExtensionMethods import ExtensionMethods
from Models.Security.User import User
from enum import Enum

#Class that manages the Security process of the system
class AuthorizationManager(object):
    userInstance = None
    def __init__(self):
        self._userInstance = AuthorizationManager.userInstance

    #Static method to check the username and password
    #Returns bool and instance of User
    @staticmethod
    def CheckUserCred(username, password):
        resultBool = False
        _user = None
        _users = ExtensionMethods.LoadData("SecurityUsers")
        if len(_users) > 0:
            _userGrep = [u for u in _users if str(u["Username"]).lower() == username.lower() and u["Password"].lower() == password.lower()]
            resultBool = len(_userGrep) > 0
            if resultBool:
                _userRow = _userGrep[0]
                _user = User(int(_userRow["_Id"]), int(_userRow["_Type"]), _userRow["Username"], _userRow["FirstName"], _userRow["LastName"])
        return resultBool, _user
    
    
    #Returns Username of the instance User that has Id equal to userId
    @staticmethod
    def GetUserNameById(userId):
        userName = ""
        _users = ExtensionMethods.LoadData("SecurityUsers")
        if len(_users) > 0:
            _userGrep = [u for u in _users if len(u["_Id"]) > 0 and int(u["_Id"]) == userId]
            resultBool = len(_userGrep) > 0
            if resultBool:
                userName = _userGrep[0]["Username"]
        return userName

    
    #Returns instance of User that has Id equal to userId
    @staticmethod
    def GetUserById(userId):
        _user = None
        _users = ExtensionMethods.LoadData("SecurityUsers")
        if len(_users) > 0:
            _userGrep = [u for u in _users if len(u["_Id"]) > 0 and int(u["_Id"]) == userId]
            if len(_userGrep) > 0:
                _userRow = _userGrep[0]
                _user = User(int(_userRow["_Id"]), int(_userRow["_Type"]), _userRow["Username"], _userRow["FirstName"], _userRow["LastName"])
        return _user

    #Sets the userInstance whos logged in to null
    @staticmethod
    def UserLogout():
        userInstance = None
        return True

    #Saves the instances of the User passed through to the SecurityUsers CSV
    #Returns bool
    @staticmethod
    def SaveUserDetail(_user):
        resultBool = False
        _users = ExtensionMethods.LoadData("SecurityUsers")
        _userGrep = [u for u in _users if len(u["_Id"]) > 0 and int(u["_Id"]) == _user.GetUserId()]
        if len(_userGrep) > 0:
            oUser = _user.GetObject()
            _resetPassword = _user.GetResetPassword()
            if _resetPassword != None:
                oUser["Password"] = _resetPassword
            else:
                oUser["Password"] = _userGrep[0]["Password"]
            del _users[_users.index(_userGrep[0])]
            _users.append(oUser)
        else:
            oUser = _user.GetObject()
            oUser["Password"] = _user.GetDefaultPassword()
            _users.append(oUser)

        locationCSV = ExtensionMethods.ConfigGetValueByKey("SecurityUsers")
        resultBool = ExtensionMethods.SaveCSV(locationCSV, _users)

        return resultBool
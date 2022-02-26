from GUIInterface.HomeGUI import *
from Classes.ExtensionMethods import ExtensionMethods
from Modules.Security.AuthorizationManager import AuthorizationManager
from Models.Security.SecurityType import SecurityType
from Modules.Exception.ExceptionManager import ExceptionManager
from Classes.CatalogueProvider import CatalogueProvider 

#Controller Class which holds the Views and Logic for Home
class HomeController(object):
    def __init__(self):
        self.__GUI = HomeGUI(self)
        self.__Auth = AuthorizationManager()
        self.__exceptionManager = ExceptionManager()
        
    #Fowards on the window to the GUI method index View
    def index(self, window):
        self.__GUI.index(window)
    
        
    #Returns access and name of button of Catalogue
    def Catalogue(self):
        return True, "Catalogue"
    
    
    #Returns access and name of button of Profile
    def Profile(self):
        return True, "Profile"
    
    #Returns access and name of button of Members
    def Members(self):
        return True, "Members"
    
    
    #Returns access and name of button of RequestItems
    def RequestItems(self):
        resultBool = False
        if AuthorizationManager.userInstance._type == SecurityType.LIBRARIAN.value:
            resultBool = True
        return resultBool, "Requested Items"
    
    #Returns access and name of button of LoanedItems
    def LoanedItems(self):
        resultBool = False
        if AuthorizationManager.userInstance._type == SecurityType.LIBRARIAN.value:
            resultBool = True
        return resultBool, "Loaned Items"
    
    #Returns access and name of button of Reports
    def Reports(self):
        resultBool = False
        if AuthorizationManager.userInstance._type == SecurityType.LIBRARIAN.value:
            resultBool = True
        return resultBool, "Reports"

    #Returns the list of loans if they are overdue
    def LoadOverdueLoans(self):
        _loans = list()
        try:
            data = ExtensionMethods.LoadData("LoanJSON")
            loans = CatalogueProvider.InitailzeLoanJSON(data)
            if AuthorizationManager.userInstance._type == SecurityType.LIBRARIAN.value:
                _overdue = [_loan for _loan in loans if _loan.IsOverdue()]
            else:
                print(loans[0].GetUserId())
                print(AuthorizationManager.userInstance.GetUserId())
                _overdue = [_loan for _loan in loans if AuthorizationManager.userInstance.GetUserId() == int(_loan.GetUserId()) and _loan.IsOverdue()]
            if len(_overdue) > 0:
                _loans = _overdue
        except Exception as ex:
            self.__exceptionManager.handleException(ex)
        return _loans
from GUIInterface.CatalogueGUI import *
from Classes.ExtensionMethods import ExtensionMethods 
from Classes.CatalogueProvider import CatalogueProvider 
from Models.Product import Product
from Models.Item.Book import Book
from Models.Catalogue import Catalogue
from Models.Security.SecurityType import SecurityType
from Modules.Security.AuthorizationManager import AuthorizationManager
from Modules.Exception.ExceptionManager import ExceptionManager

#Controller Class which holds the Views and Logic for Catalogue
class CatalogueController(object):
    def __init__(self):
        self.__GUI = CatalogueGUI(self)
        self.__Auth = AuthorizationManager()
        self.__exceptionManager = ExceptionManager()
        self.__catalogue = None
        
    #Fowards on the window to the GUI method index View
    def index(self, window):
        self.__GUI.index(window)
        
    #Fowards on the window and product to the GUI method product View
    def Product(self, window, product):
        self.__GUI.ProductView(window, product)
        
    #Sets in the local instance __catalogue to the updated catalogue
    def loadCatalogue(self):
        self.__catalogue = CatalogueProvider.GetCatalogue()
        
    #Lookups up instance __catalogue against the search parameter
    def searchCatalogue(self, search):
        results = []
        if (self.__catalogue is not None):
            results = self.__catalogue.searchProduct(search)
        return results

    #Creates an item request from the product passed through
    def createItemRequest(self, product):
        resultBool = False
        returnMsg = ""
        try:
            _itemRequest = ItemRequest.CreateRequest(product)
            if _itemRequest is not None:
                resultBool = CatalogueProvider.addItemRequest(_itemRequest)
                if resultBool:
                    returnMsg = "Your request has been created. Please wait while an Admin review the request."
                else:
                    returnMsg = "Sorry but you have an request already."
        except Exception as ex:
            returnMsg = "Sorry something went wrong."
            self.__exceptionManager.handleException(ex)
        return resultBool, returnMsg
    
    #Checks the user logged in if is a Librarian
    def AdminPermission(self):
        resultBool = False
        if AuthorizationManager.userInstance._type == SecurityType.LIBRARIAN.value:
            resultBool = True
        return resultBool
    
    #Saves the edit item into the stockJSON
    def saveItem(self, _item):
        resultBool = False
        returnMsg = ""
        try:
            resultBool = CatalogueProvider.editItem(_item)
            if resultBool:
                returnMsg = "Your product has been saved."
            else:
                returnMsg = "Sorry something went wrong."
        except Exception as ex:
            returnMsg = "Sorry something went wrong."
            self.__exceptionManager.handleException(ex)
        return resultBool, returnMsg
    
    #Add the new created instance of Product into the stockJSON
    def addItem(self, _item):
        resultBool = False
        returnMsg = ""
        try:
            resultBool = CatalogueProvider.addItem(_item)
            if resultBool:
                returnMsg = "Your product has been added."
            else:
                returnMsg = "Sorry something went wrong."
        except Exception as ex:
            returnMsg = "Sorry something went wrong."
            self.__exceptionManager.handleException(ex)
        return resultBool, returnMsg
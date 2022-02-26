from GUIInterface.AdminGUI import *
from Classes.ExtensionMethods import ExtensionMethods
from Classes.CatalogueProvider import CatalogueProvider
import datetime
from Models.Loan import Loan
from Modules.Security.AuthorizationManager import AuthorizationManager
from Models.Security.SecurityType import SecurityType
from Modules.Exception.ExceptionManager import ExceptionManager

#Controller Class which holds the Views and Logic for Admin
class AdminController(object):
    def __init__(self):
        self.__GUI = AdminGUI(self)
        self.__Auth = AuthorizationManager()
        self.__exceptionManager = ExceptionManager()
   
    #Fowards on the window to the GUI method Request View
    def Request(self, window):
        self.__GUI.RequestView(window)
        
    #Fowards on the window to the GUI method Loaned View
    def Loaned(self, window):
        self.__GUI.LoanedView(window)
        
    #Fowards on the window to the GUI method Loaned Report View
    def LoanedReport(self, window):
        self.__GUI.LoanReportView(window)
    
    #Creates the loan report and saves it within the ReportDownload folder
    def LoadLoanedReport(self):
        resultBool = False
        try:
                data = ExtensionMethods.LoadData("LoanJSON")
                loans = CatalogueProvider.InitailzeLoanJSON(data)
                _loanReport = list()
                for _loan in loans:
                     if _loan.IsOverdue():
                         isOverdue = "Yes"
                     else:
                         isOverdue = "No"

                     _loanReport.append({
                                "Member": _loan.GetUsername()
                                , "Item": _loan.GetProduct().name
                                , "Date Loaned": _loan.GetCreatedDateAsString()
                                , "Date To Return": _loan.GetReturnDateAsString()
                                , "IsOverdue": isOverdue
                            })

                fileLocation = ExtensionMethods.AppSettingGetValueByKey("ReportDownload")
                fileName = ("Loan_Report" + datetime.datetime.now(datetime.timezone.utc).strftime("%d_%M_%Y_%H_%M_%S") + ".csv")
                resultBool = ExtensionMethods.CreateCSV(fileLocation, fileName, _loanReport)

        except Exception as ex:
            self.__exceptionManager.handleException(ex)
        return resultBool
    
    #Creates the request report and saves it within the ReportDownload folder
    def LoadRequestReport(self):
        resultBool = False
        try:
                data = ExtensionMethods.LoadData("RequestJSON")
                itemRequests = CatalogueProvider.InitailzeItemRequestJSON(data)
                _requestReport = list()
                for itemRequest in itemRequests:
                    _requestReport.append({
                                "Member": itemRequest.GetUsername()
                                , "Item": itemRequest.GetProduct().name
                                , "Date Requested": itemRequest.GetDateAsString()
                            })
                fileLocation = ExtensionMethods.AppSettingGetValueByKey("ReportDownload")
                fileName = ("Request_Report" + datetime.datetime.now(datetime.timezone.utc).strftime("%d_%M_%Y_%H_%M_%S") + ".csv")
                resultBool = ExtensionMethods.CreateCSV(fileLocation, fileName, _requestReport)

        except Exception as ex:
            self.__exceptionManager.handleException(ex)
        return resultBool

    
    #Creates the stock report and saves it within the ReportDownload folder
    def LoadStockReport(self):
        resultBool = False
        try:
                _stockData = ExtensionMethods.LoadData("StockJSON")
                fileLocation = ExtensionMethods.AppSettingGetValueByKey("ReportDownload")
                fileName = ("Stock_Report" + datetime.datetime.now(datetime.timezone.utc).strftime("%d_%M_%Y_%H_%M_%S") + ".csv")
                resultBool = ExtensionMethods.CreateCSV(fileLocation, fileName, _stockData)

        except Exception as ex:
            self.__exceptionManager.handleException(ex)
        return resultBool

    #Creates the Members report and saves it within the ReportDownload folder
    def LoadMembersReport(self):
        resultBool = False
        try:
                _users = ExtensionMethods.LoadData("SecurityUsers")
                fileLocation = ExtensionMethods.AppSettingGetValueByKey("ReportDownload")
                fileName = ("Members_Report" + datetime.datetime.now(datetime.timezone.utc).strftime("%d_%M_%Y_%H_%M_%S") + ".csv")
                resultBool = ExtensionMethods.CreateCSV(fileLocation, fileName, _users)

        except Exception as ex:
            self.__exceptionManager.handleException(ex)
        return resultBool
    
    
    #Returns the Requests within a list from the data RequestJSON
    def LoadRequests(self):
        itemRequests = list()
        try:
            data = ExtensionMethods.LoadData("RequestJSON")
            itemRequests = CatalogueProvider.InitailzeItemRequestJSON(data)
        except Exception as ex:
            self.__exceptionManager.handleException(ex)
        return itemRequests
    
    #Returns the Loans within a list from the data LoanJSON
    def LoadLoans(self):
        loans = list()
        try:
            data = ExtensionMethods.LoadData("LoanJSON")
            loans = CatalogueProvider.InitailzeLoanJSON(data)
        except Exception as ex:
            self.__exceptionManager.handleException(ex)
        return loans

    
    #Accepts Request and updates the stock of the product from the request
    def AcceptRequest(self, itemRequest):
        resultBool = False
        _product = itemRequest.GetProduct()
        _stockCheck = _product.stockCheck(1)
        if _stockCheck:
            _product.removeStock(1)
            resultBool = CatalogueProvider.UpdateProductCatalogue(_product)
            if resultBool:
                CatalogueProvider.removeItemRequest(itemRequest)
                _user = itemRequest.GetUser()
                _loan = Loan.CreateLoan(_product, _user)
                if _loan != None:
                    resultBool = CatalogueProvider.addLoan(_loan)
        return resultBool
    
    #Decline Request
    def DeclineRequest(self, itemRequest):
        return CatalogueProvider.removeItemRequest(itemRequest)
    
    #Remove loan from list and updates stock of product within loan
    def ReturnedLoan(self, _loan):
        resultBool = False
        _product = _loan.GetProduct()
        _product.addStock(1)
        resultBool = CatalogueProvider.UpdateProductCatalogue(_product)
        if resultBool:
            CatalogueProvider.removeLoan(_loan)
        return resultBool
        

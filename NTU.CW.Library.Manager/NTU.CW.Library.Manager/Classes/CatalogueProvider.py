from json import *
from Classes.ExtensionMethods import ExtensionMethods 
from Models.Product import Product
from Models.Item.Book import Book
from Models.Item.Journal import Journal
from Models.Item.CD import CD
from Models.Catalogue import Catalogue

#Static class Catalogue
#Has static methods for features of the catalogue, getting, updating and deleteting items
class CatalogueProvider:

    #Returns instance of Catalogue with the data from json file
    @staticmethod
    def GetCatalogue():
        _catalogue = Catalogue(None)
        _stockData = ExtensionMethods.LoadData("StockJSON")
        for item in _stockData:
            if item["Type"] == "book":
                _book = CatalogueProvider.createBookInstance(item)
                _catalogue.addProduct(_book)
            if item["Type"] == "journal":
                _journal = CatalogueProvider.createJournalInstance(item)
                _catalogue.addProduct(_journal)
            if item["Type"] == "cd":
                _cd = CatalogueProvider.createCDInstance(item)
                _catalogue.addProduct(_cd)
        return _catalogue

    #Updates the stock json with the product passed
    @staticmethod
    def UpdateProductCatalogue(_product):
        _result = False
        _stockData = ExtensionMethods.LoadData("StockJSON")
        _dict = [p for p in _stockData if p["_Id"] == _product.GetId()][0]
        _dict["AvaibleStock"] = _product.getAvStcok()
        _dict["Stock"] = _product.stock
        fileLocation = ExtensionMethods.ConfigGetValueByKey("StockJSON")
        ExtensionMethods.SaveJSON(fileLocation, _stockData)
        _result = True
        return _result
    
    #Gets the product stock from the stock json
    @staticmethod
    def GetProductCatalogueStock(_product):
        _stockAv = _product.getAvStcok()
        _stockData = ExtensionMethods.LoadData("StockJSON")
        _dict = [p for p in _stockData if p["_Id"] == _product.GetId()][0]
        if _dict != None:
            _stockAv = _product.setAvStock(_dict["AvaibleStock"])
        return _stockAv

    #Creates and returns a instance of a book
    @staticmethod
    def createBookInstance(item):
        id = item["_Id"]
        title = item["Title"]
        author = item["Author"]
        sku = item["SKU"]
        stock = int(item["Stock"])
        avstock = int(item["AvaibleStock"])
        return Book(id, title, author, sku, stock, avstock)

    #Creates and returns a instance of a Journal
    @staticmethod
    def createJournalInstance(item):
        id = item["_Id"]
        title = item["Title"]
        author = item["Author"]
        sku = item["SKU"]
        stock = int(item["Stock"])
        avstock = int(item["AvaibleStock"])
        return Journal(id, title, author, sku, stock, avstock)

     #Creates and returns a instance of a CD
    @staticmethod
    def createCDInstance(item):
        id = item["_Id"]
        title = item["Title"]
        author = item["Author"]
        sku = item["SKU"]
        stock = int(item["Stock"])
        avstock = int(item["AvaibleStock"])
        return CD(id, title, author, sku, stock, avstock)


    #With the json pass through it initailze it into a instance of list<ItemRequest>
    @staticmethod
    def InitailzeItemRequestJSON(jsonData):
        from Models.ItemRequest import ItemRequest
        _itemRequests = list()
        if len(jsonData) > 0:
            for item in jsonData:
                utcDateTime = item["_CreatedDateTime"]
                from datetime import datetime
                _datetime = datetime.strptime(utcDateTime, '%d/%m/%Y')
                itemRequest = ItemRequest(item["SecurityUserId"], item["ProductId"], item["_Id"], _datetime)
                _itemRequests.append(itemRequest)
        return _itemRequests

    
    #With the json pass through it initailze it into a instance of list<Loan>
    @staticmethod
    def InitailzeLoanJSON(jsonData):
        from Models.Loan import Loan
        _loans = list()
        if len(jsonData) > 0:
            for item in jsonData:
                _createdDateTimeStr = item["_CreatedDateTime"]
                _returnDateTimeStr = item["_ReturnDateTime"]
                from datetime import datetime
                _createdDateTime = datetime.strptime(_createdDateTimeStr, '%d/%m/%Y')
                _returnDateTime = datetime.strptime(_returnDateTimeStr, '%d/%m/%Y')
                _loan = Loan(item["SecurityUserId"], item["ProductId"], item["_Id"], _createdDateTime, _returnDateTime)
                _loans.append(_loan)
        return _loans

    #Appends to the RequestJSON file the itemRequest passed through
    @staticmethod
    def addItemRequest(itemRequest):
        resultBool = False
        data = ExtensionMethods.LoadData("RequestJSON")
        _saveBool = True
        itemRequestIdentity = 1
        if len(data) > 0: 
            if len([u for u in data if u["SecurityUserId"] == str(itemRequest.GetUserId()) and u["ProductId"] == str(itemRequest.GetProductId())]) > 0:
                _saveBool = False
            else:
                itemTop = sorted(data, key = lambda i: (i['_Id']))[0]
                itemRequestIdentity = int(itemTop["_Id"]) + 1
        if _saveBool:
            itemRequest.SetId(itemRequestIdentity)
            data.append(itemRequest.GetObject())
            fileLocation = ExtensionMethods.ConfigGetValueByKey("RequestJSON")
            resultBool = ExtensionMethods.SaveJSON(fileLocation, data)
        return resultBool
    
    #Removes to the RequestJSON file the itemRequest passed through
    @staticmethod
    def removeItemRequest(itemRequest):
        resultBool = False
        data = ExtensionMethods.LoadData("RequestJSON")
        itemRequestIdentity = itemRequest.GetId()
        if len(data) > 0: 
            _itemReq = [u for u in data if u["_Id"] == itemRequestIdentity]
            if len(_itemReq) > 0:
                del data[data.index(_itemReq[0])]
        fileLocation = ExtensionMethods.ConfigGetValueByKey("RequestJSON")
        resultBool = ExtensionMethods.SaveJSON(fileLocation, data)
        return resultBool

    
    #Appends to the LoanJSON file the Loan passed through
    @staticmethod
    def addLoan(_loan):
        resultBool = False
        data = ExtensionMethods.LoadData("LoanJSON")
        _saveBool = True
        loanIdentity = 1
        if len(data) > 0: 
            if len([u for u in data if u["SecurityUserId"] == str(_loan.GetUserId()) and u["ProductId"] == str(_loan.GetProductId())]) > 0:
                _saveBool = False
            else:
                itemTop = sorted(data, key = lambda i: (i['_Id']))[0]
                loanIdentity = int(itemTop["_Id"]) + 1
        if _saveBool:
            _loan.SetId(loanIdentity)
            _loanObj = _loan.GetObject()
            data.append(_loanObj)
            CatalogueProvider.addHistory("Loan", _loanObj)
            fileLocation = ExtensionMethods.ConfigGetValueByKey("LoanJSON")
            resultBool = ExtensionMethods.SaveJSON(fileLocation, data)
        return resultBool

    

    
    #Edit the item to the StockJSON file the Item passed through
    @staticmethod
    def editItem(_item):
        resultBool = False
        data = ExtensionMethods.LoadData("StockJSON")
        _id = _item.GetId()
        if len(data) > 0:
            itemGrep = [u for u in data if u["_Id"] == _id]
            if len(itemGrep) > 0:
                itemJSON = itemGrep[0]
                itemJSON["Title"] = _item.name
                itemJSON["Author"] = _item.owner
                itemJSON["Stock"] = _item.stock
                itemJSON["AvaibleStock"] = _item.getAvStcok()
                del data[data.index(itemGrep[0])]
                data.append(itemJSON)
                fileLocation = ExtensionMethods.ConfigGetValueByKey("StockJSON")
                resultBool = ExtensionMethods.SaveJSON(fileLocation, data)
        return resultBool

    @staticmethod
    def addItem(_item):
        resultBool = False
        data = ExtensionMethods.LoadData("StockJSON")
        itemIdentity = 1
        if len(data) > 0: 
            itemTop = sorted(data, key = lambda i: (i['_Id']))[0]
            itemIdentity = int(itemTop["_Id"]) + 1
        itemJSON = {}
        itemJSON["Type"] = _item.GetType()
        itemJSON["_Id"] = itemIdentity
        itemJSON["SKU"] = _item.GenerateSKU(itemIdentity)
        itemJSON["Title"] = _item.name
        itemJSON["Author"] = _item.owner
        itemJSON["Stock"] = _item.stock
        itemJSON["AvaibleStock"] = _item.getAvStcok()
        data.append(itemJSON)
        fileLocation = ExtensionMethods.ConfigGetValueByKey("StockJSON")
        resultBool = ExtensionMethods.SaveJSON(fileLocation, data)
        return resultBool
    
    #Removes to the LoanJSON file the Loan passed through
    @staticmethod
    def removeLoan(_loan):
        resultBool = False
        data = ExtensionMethods.LoadData("LoanJSON")
        loanIdentity = _loan.GetId()
        if len(data) > 0: 
            _loanD = [u for u in data if u["_Id"] == loanIdentity]
            if len(_loanD) > 0:
                del data[data.index(_loanD[0])]
        fileLocation = ExtensionMethods.ConfigGetValueByKey("LoanJSON")
        resultBool = ExtensionMethods.SaveJSON(fileLocation, data)
        return resultBool
    
    #Appends to the HistoryJSON file the type of object passed through
    @staticmethod
    def addHistory(_type, _object):
        data = ExtensionMethods.LoadData("HistoryJSON")
        _object["Type"] = _type
        data.append(_object)
        fileLocation = ExtensionMethods.ConfigGetValueByKey("HistoryJSON")
        resultBool = ExtensionMethods.SaveJSON(fileLocation, data)

    #Gets from the catalogue the product by id
    @staticmethod
    def GetProductById(productId):
        _product = None
        _catalogue = CatalogueProvider.GetCatalogue()
        _product = _catalogue.GetProductById(productId)
        return _product


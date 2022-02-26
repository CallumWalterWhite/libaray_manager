class Product(object):
    def __init__(self, _id, _type, owner, name, stock, avstock):
        self.__id = _id
        self._type = _type
        self.stock = stock
        self.owner = owner
        self.name = name
        self.__avsotck = avstock

    def GetId(self):
        return int(self.__id)

    def GetStrId(self):
        return str(self.__id)

    def GetType(self):
        return str(self._type)


    def __updateStock(self):
        from Classes.CatalogueProvider import CatalogueProvider
        CatalogueProvider.GetProductCatalogueStock(self)
        

    def stockCheck(self, amount):
        boolResult = False
        try:
            self.__updateStock()
            if (self.__avsotck - amount) >= 0:
                boolResult = True
        except Exception as ex:
            pass
        return boolResult
    
    def addStock(self, amount):
        boolResult = False
        self.__updateStock()
        self.__avsotck += amount
        if self.stock < self.__avsotck:
            self.stock = self.__avsotck
            boolResult = True
        return boolResult


    def removeStock(self, amount):
        boolResult = False
        self.__updateStock()
        if self.stockCheck(amount):
            self.__avsotck = self.__avsotck - amount
            boolResult = True
        return boolResult
    
    def productStockAvLbl(self):
        return str.format("Stock Available - {}".format(str(self.__avsotck)))
    
    def getAvStcok(self):
        return self.__avsotck

    def setAvStock(self, _avStock):
        self.__avsotck == _avStock
        return self.__avsotck

    def GenerateSKU(self, id):
        _sku = ""
        if self._type.lower() == "book":
            _sku = str.format("BK-{}-{}", self.name[0:2], id)
        if self._type.lower() == "cd": 
            _sku = str.format("CD-{}-{}", self.name[0:2], id)
        if self._type.lower() == "journal":
            _sku = str.format("jg-{}-{}", self.name[0:2], id)
        return _sku
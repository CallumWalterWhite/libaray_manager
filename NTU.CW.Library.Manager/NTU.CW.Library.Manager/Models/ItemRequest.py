import datetime
from Modules.Security.AuthorizationManager import AuthorizationManager
from Classes.CatalogueProvider import CatalogueProvider 

class ItemRequest(object):
    def __init__(self, userId, productId, _id = 0, _datetime = datetime.datetime.now(datetime.timezone.utc)):
        if userId is not None and productId is not None:
            self.__id = int(_id)
            self.__datetime = _datetime
            self.__userId = int(userId)
            self.__productId = int(productId)
            self.__product = None

    @staticmethod
    def CreateRequest(product, amount=1, user=None):
        if user is None:
            user = AuthorizationManager.userInstance
        _itemRequest = None
        if product.stockCheck(amount):
            _itemRequest = ItemRequest(user.GetUserId(), product.GetId())
        return _itemRequest

    def SetId(self, _id):
        self.__id = _id

    def GetId(self):
        return self.__id

    def GetProductId(self):
        return self.__productId

    def GetProduct(self):
        self.__setProduct()
        return self.__product

    def GetUserId(self):
        return self.__userId

    def GetUser(self):
        return AuthorizationManager.GetUserById(self.__userId)

    def GetUsername(self):
        return AuthorizationManager.GetUserNameById(self.__userId)
    
    def GetDateAsString(self):
        return (self.__datetime.strftime("%d/%m/%Y"))

    def __setProduct(self):
        self.__product = CatalogueProvider.GetProductById(self.__productId)

    def GetTitle(self):
        _title = ""
        _username = AuthorizationManager.GetUserNameById(self.__userId)
        self.__setProduct()
        if self.__product is not None:
            _title = str.format("User - {0} | Product - {1}".format(_username, self.__product.name))
        return _title

    def GetObject(self):
        _obj = {
            "_Id":  self.__id,
            "_CreatedDateTime": (self.__datetime.strftime("%d/%m/%Y")),
            "SecurityUserId": str(self.__userId),
            "ProductId": str(self.__productId)
          }
        return _obj
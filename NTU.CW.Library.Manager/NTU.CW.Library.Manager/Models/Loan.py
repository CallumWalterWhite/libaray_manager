import datetime
from Modules.Security.AuthorizationManager import AuthorizationManager
from Classes.CatalogueProvider import CatalogueProvider 

class Loan(object):
    def __init__(self, userId, productId, _id = 0, createddatetime = datetime.datetime.now(datetime.timezone.utc), returndatetime = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=14))):
        if userId is not None and productId is not None:
            self.__id = int(_id)
            self.__createddatetime = createddatetime
            self.__returndatetime = returndatetime
            self.__userId = int(userId)
            self.__productId = int(productId)
            self.__product = None
            
    @staticmethod
    def CreateLoan(product, user=None):
        if user is None:
            user = AuthorizationManager.userInstance
        _loan = Loan(user.GetUserId(), product.GetId())
        return _loan

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

    def IsOverdue(self):
        return self.__returndatetime.date() < datetime.datetime.now(datetime.timezone.utc).date()

    def GetUsername(self):
        return AuthorizationManager.GetUserNameById(self.__userId)

    def GetCreatedDateAsString(self):
        return (self.__createddatetime.strftime("%d/%m/%Y"))
    
    def GetReturnDateAsString(self):
        return (self.__returndatetime.strftime("%d/%m/%Y"))

    def __setProduct(self):
        self.__product = CatalogueProvider.GetProductById(self.__productId)
        
    def GetTitle(self):
        _title = ""
        _username = AuthorizationManager.GetUserNameById(self.__userId)
        self.__setProduct()
        if self.__product is not None:
            if self.IsOverdue():
                _title = str.format("Overdue! - User - {0} | Product - {1} | To Return Date - {2}".format(_username, self.__product.name, self.__returndatetime.strftime("%d/%m/%Y")))
            else:
                _title = str.format("User - {0} | Product - {1} | To Return Date - {2}".format(_username, self.__product.name, self.__returndatetime.strftime("%d/%m/%Y")))
            
        return _title

    def GetObject(self):
        _obj = {
            "_Id":  self.__id,
            "_CreatedDateTime": (self.__createddatetime.strftime("%d/%m/%Y")),
            "_ReturnDateTime": (self.__returndatetime.strftime("%d/%m/%Y")),
            "SecurityUserId": str(self.__userId),
            "ProductId": str(self.__productId)
          }
        return _obj
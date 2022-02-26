import unittest
from Classes.RouteConfig import RouteConfig
from Classes.ExtensionMethods import ExtensionMethods
from Modules.Security.AuthorizationManager import AuthorizationManager
import hashlib


class TestSecurity(unittest.TestCase):
    def test_login(self):
        password = "Test"
        hashPWObj = hashlib.md5(password.encode())
        _password = hashPWObj.hexdigest()
        resultBool, _user = AuthorizationManager.CheckUserCred("Librarian", _password)
        if resultBool:
            AuthorizationManager.userInstance = _user
        self.assertTrue(resultBool)

 
class TestCatalogue(unittest.TestCase):
    def test_additem(self):
        from Models.Product import Product
        from Classes.CatalogueProvider import CatalogueProvider
        product = Product(-1, "book", "test", "unit test book", 5, 5)
        resultBool = CatalogueProvider.addItem(product)
        self.assertTrue(resultBool)

    def test_edititem(self):
        from Models.Product import Product
        from Classes.CatalogueProvider import CatalogueProvider
        _testCatalogue = CatalogueProvider.GetCatalogue()
        if _testCatalogue.Length() > 0:
            _testItem = _testCatalogue.GetProductById(1)
            _testItem.name = "Test"
            resultBool = CatalogueProvider.editItem(_testItem)
            self.assertTrue(resultBool)

    def test_additemrequest(self):
        from Models.Product import Product
        from Classes.CatalogueProvider import CatalogueProvider
        from Models.ItemRequest import ItemRequest
        password = "Test"
        hashPWObj = hashlib.md5(password.encode())
        _password = hashPWObj.hexdigest()
        resultBool, _user = AuthorizationManager.CheckUserCred("Member", _password)
        _testCatalogue = CatalogueProvider.GetCatalogue()
        if _testCatalogue.Length() > 0:
            _testItem = _testCatalogue.GetProductById(1)
            _itemRequest = ItemRequest.CreateRequest(_testItem, 1, _user)
            if _itemRequest is not None:
                resultBool = CatalogueProvider.addItemRequest(_itemRequest)
                self.assertTrue(resultBool)
 
    

if __name__ == '__main__':
    RouteConfig.UnitTestState = 1
    unittest.main()
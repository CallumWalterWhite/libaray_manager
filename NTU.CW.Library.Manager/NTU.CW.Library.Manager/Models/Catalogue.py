
#Class holds the Products within the system
#Contain methods to lookup products
class Catalogue(object):
    def __init__(self, stock=None):
        if stock == None: 
            self._stock = list()
        else:               
            self._stock = stock

    #Add its property _stock the product passed through
    def addProduct(self, product):
        try:
            self._stock.append(product)
        except Exception as ex:
            exceptionManger.handleException(ex, ExceptionPolicy._policyLogAndCotinue)

    #Returns the products within its property _stock against the input passed through
    def searchProduct(self, _input):
        stockSearch = [x for x in self._stock if _input.lower() in x.name.lower() or _input.lower() in x.owner.lower()]
        return stockSearch

    #Returns the product that has the id passed through
    def GetProductById(self, _id):
        _product = None
        _products = [x for x in self._stock if int(_id) == x.GetId()]
        if len(_products) > 0:
            _product = _products[0]
        return _product
    
    def Length(self):
        return len(self._stock)
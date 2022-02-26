from Product import Product

#Class holds information for type of product Book, parent class is Product
class Book(Product):
    def __init__(self, _id, title, author, sku, stock, avstock):
        self.__productId = _id
        self.title = title
        self.author = author
        self.sku = sku
        self.stock = stock
        self.avstock = avstock
        self.__sup()

    #Initailze the instance of Book with its parent class to inherit its methods
    def __sup(self):
        super(Book, self).__init__(self.__productId, type(self), self.author, self.title, self.stock, self.avstock)

    def ProductView(self):
        _views = [self.__productType(), self.__productTitle(), self.__productAuthor()]
        return _views

    def ProductTitle(self):
        return str.format("Product - {0} | {1}".format(self.author, self.title))
    
    def __productType(self):
        return str("Type - Book")

    def __productTitle(self):
        return str.format("Title - {0}".format(self.title))
    
    def __productAuthor(self):
        return str.format("Author - {0}".format(self.author))
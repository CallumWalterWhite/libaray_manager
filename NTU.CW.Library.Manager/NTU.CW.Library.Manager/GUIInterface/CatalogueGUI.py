from Packages.tkinter import *
from Classes.ExtensionMethods import ExtensionMethods
from Models.ItemRequest import ItemRequest
from Modules.Exception.ExceptionManager import ExceptionManager

class CatalogueGUI(object):
    def __init__(self, controller, tk=None):
        self.__controller = controller
        self.__instanceListSelect = None
        self.__exceptionManager = ExceptionManager()
        
    #Renders the window to show a list of products with a searhable box which will returns products to fit the criteria entered
    #Users will be able to click the products to view them
    #User with admin permissions will be able to see add item button
    def index(self, window):
        try:

            ExtensionMethods.ClearTkWindow(window)
            self.__controller.loadCatalogue()
            def _back():
                ExtensionMethods.Redirect("Home", "index", window)
            Button(window, text="Back", command=_back).pack()
            ExtensionMethods.DefaultBlankSpace(window)
            top = window
            top.title('Catalogue')
        
            Label(text="Search for product by title or author", width="300", height="2", font=("Calibri", 13)).pack() 
            ExtensionMethods.DefaultBlankSpace(window)

            listbox = Listbox(top, width=50)
            listbox.pack()

            def productSearch():
                try:
                    searchInput = name_box.get()
                    results = self.__controller.searchCatalogue(searchInput)
                    listbox.delete(0,'end')
                    if (len(results) > 0):
                        self.__instanceListSelect = results
                        for item in results:
                            _productTitle = (item.name +  " - " + item.owner)
                            listbox.insert(0, _productTitle)
                    else:
                            self.__instanceListSelect = None
                            listbox.insert(0, "Search Results Empty")
                except Exception as ex:
                    self.__exceptionManager.handleException(ex) 

            def onProductSelect(event):
                try:
                    if len(self.__instanceListSelect) > 0:
                        index = int(listbox.curselection()[0]) + 1
                        productSelected = self.__instanceListSelect[len(self.__instanceListSelect) - index]
                        self.__controller.Product(window, productSelected)
                except Exception as ex:
                    self.__exceptionManager.handleException(ex) 

            def addProduct():
                self.ProductAdd(window)

            listbox.bind('<<ListboxSelect>>', onProductSelect)
        
            ExtensionMethods.DefaultBlankSpace(window)
            name_box = Entry()
            name_box.pack()
            ExtensionMethods.DefaultBlankSpace(window)
            button = Button(top, text="Search For Product", command=productSearch)
            button.pack()

                
            if self.__controller.AdminPermission():
                button = Button(window, text="Add Item", command=addProduct)
                button.pack()

            mainloop()
        except Exception as ex:
            self.__exceptionManager.handleException(ex)
            
    #Renders the window to show the product passed through
    #Users will be able to click the request button to create an request
    #User with admin permissions will be able to see edit item button
    def ProductView(self, window, product):
        ExtensionMethods.ClearTkWindow(window)
        def _back():
            ExtensionMethods.Redirect("Catalogue", "index", window)
        Button(window, text="Back", command=_back).pack()
        window.title(product.name)
        
        warning = StringVar()
        editWarning = StringVar()
        Label(text=product.ProductTitle(), width="300", height="2", font=("Calibri", 13)).pack()
        ExtensionMethods.DefaultBlankSpace(window)
        _views = product.ProductView()
        for vi in _views:
            Label(text=vi, width="300", background='lightblue', height="1", font=("Calibri", 9)).pack() 

        Label(text=product.productStockAvLbl(), width="300", background='lightblue', height="1", font=("Calibri", 9)).pack() 

        _avStock = product.getAvStcok()

        def request():
            resultBool, returnMsg = self.__controller.createItemRequest(product)
            warning.set(returnMsg)

            
        def edit():
            self.ProductEdit(window, product)


        if _avStock > 0:
            ExtensionMethods.DefaultBlankSpace(window)
            button = Button(window, text="Request Item", command=request)
            button.pack()
            Label(window, background='lightblue', textvariable=warning).pack()

        if self.__controller.AdminPermission():
            button = Button(window, text="Edit Item", command=edit)
            button.pack()
            Label(window, background='lightblue', textvariable=editWarning).pack()



        mainloop()

        
    #Renders the window to show the product passed through for editing
    def ProductEdit(self, window, product):
        ExtensionMethods.ClearTkWindow(window)
        def _back():
            ExtensionMethods.Redirect("Catalogue", "index", window)
        Button(window, text="Back", command=_back).pack()
        window.title(product.name)
        
        warning = StringVar()
        productView = product.ProductView()
        strType = productView[0]
        type_label = Label(window, text=strType)
        type_label.pack()
        strId = str.format("Id - {}", product.GetStrId())
        id_label = Label(window, text=strId)
        id_label.pack()

        stock = StringVar()
        owner = StringVar()
        avstock = StringVar()
        name = StringVar()

        stock.set(product.stock)
        owner.set(product.owner)
        name.set(product.name)
        avstock.set(product.getAvStcok())


        name_label = Label(window, text="Name")
        name_label.pack()
 
        name_entry = Entry(window, textvariable=name)
        name_entry.pack()

        owner_label = Label(window, text="Owner")
        owner_label.pack()
 
        owner_entry = Entry(window, textvariable=owner)
        owner_entry.pack()

        
        stock_label = Label(window, text="Stock")
        stock_label.pack()
 
        stock_entry = Entry(window, textvariable=stock)
        stock_entry.pack()
        
        avstock_label = Label(window, text="Available Stock")
        avstock_label.pack()
 
        avstock_entry = Entry(window, textvariable=avstock)
        avstock_entry.pack()

        def save():
            product.name = name.get()
            product.owner = owner.get()
            product.stock = stock.get()
            product.setAvStock(avstock.get())
            resultBool, returnMsg = self.__controller.saveItem(product)
            warning.set(returnMsg)

        ExtensionMethods.DefaultBlankSpace(window)
        button = Button(window, text="Save", command=save)
        button.pack()
        Label(window, background='lightblue', textvariable=warning).pack()




        mainloop()

        
    #Renders the window to show an entry for creating an Product
    def ProductAdd(self, window):
        ExtensionMethods.ClearTkWindow(window)
        def _back():
            ExtensionMethods.Redirect("Catalogue", "index", window)
        Button(window, text="Back", command=_back).pack()
        window.title("Add Product")
        
        warning = StringVar()
        stock = StringVar()
        owner = StringVar()
        avstock = StringVar()
        name = StringVar()
        _type = StringVar()

        name_label = Label(window, text="Name")
        name_label.pack()
 
        name_entry = Entry(window, textvariable=name)
        name_entry.pack()

        owner_label = Label(window, text="Owner")
        owner_label.pack()
 
        owner_entry = Entry(window, textvariable=owner)
        owner_entry.pack()

        
        stock_label = Label(window, text="Stock")
        stock_label.pack()
 
        stock_entry = Entry(window, textvariable=stock)
        stock_entry.pack()
        
        avstock_label = Label(window, text="Available Stock")
        avstock_label.pack()
 
        avstock_entry = Entry(window, textvariable=avstock)
        avstock_entry.pack()

        type_label = Label(window, text="Type")
        type_label.pack()

        
        _type_label = Label(window, text="Please choose from Book, CD, Journal")
        _type_label.pack()

        
        type_entry = Entry(window, textvariable=_type)
        type_entry.pack()

        def add():
            from Models.Product import Product
            product = Product(-1, _type.get().lower(), owner.get(), name.get(), stock.get(), avstock.get())
            resultBool, returnMsg = self.__controller.addItem(product)
            warning.set(returnMsg)

        ExtensionMethods.DefaultBlankSpace(window)
        button = Button(window, text="Add", command=add)
        button.pack()
        Label(window, background='lightblue', textvariable=warning).pack()

        mainloop()



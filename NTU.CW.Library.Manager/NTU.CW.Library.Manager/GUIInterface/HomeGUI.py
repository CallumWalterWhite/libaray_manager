from Packages.tkinter import *
from Classes.ExtensionMethods import ExtensionMethods

class HomeGUI(object):
    def __init__(self, controller):
        self.__controller = controller

    #Renders the window to show buttons for users to click to be redirected to different modules
    def index(self, window):
        ExtensionMethods.ClearTkWindow(window)

        window.title("Home")
        Label(window, text=ExtensionMethods.GetUserName()).pack()
        ExtensionMethods.DefaultBlankSpace(window)
        _overdueLoans = self.__controller.LoadOverdueLoans();
        
        def __createMenuOption(window, controllerMethod, callback):
            resultBool, _text = getattr(self.__controller, controllerMethod)()
            if resultBool:
                Button(window, text=_text, width=20, height=5, command=callback).pack()

        def _catalogueEvent():
            ExtensionMethods.Redirect("Catalogue", "index", window)
            
        def _requestItemEvent():
            ExtensionMethods.Redirect("Admin", "Request", window)
            
        def _profileEvent():
            ExtensionMethods.Redirect("Security", "Profile", window)
        
        def _memberEvent():
            ExtensionMethods.Redirect("Security", "Members", window)
        
        def _loanedItemEvent():
            ExtensionMethods.Redirect("Admin", "Loaned", window)
        
        def _reportsEvent():
            ExtensionMethods.Redirect("Admin", "LoanedReport", window)

        
        def _logoutEvent():
            ExtensionMethods.Redirect("Security", "Logout", window)

        __createMenuOption(window, "Catalogue", _catalogueEvent)
        __createMenuOption(window, "Profile", _profileEvent)
        __createMenuOption(window, "Members", _memberEvent)
        __createMenuOption(window, "RequestItems", _requestItemEvent)
        __createMenuOption(window, "LoanedItems", _loanedItemEvent)
        __createMenuOption(window, "Reports", _reportsEvent)

        if len(_overdueLoans) > 0:
            Label(window, background='lightblue', text="Notifcation - ").pack()
            for _loan in _overdueLoans:
                _title = _loan.GetTitle()
                Label(window, background='lightblue', text=_title).pack()

        Button(window, text="Logout", width=10, height=1, command=_logoutEvent).pack()

        window.mainloop() 


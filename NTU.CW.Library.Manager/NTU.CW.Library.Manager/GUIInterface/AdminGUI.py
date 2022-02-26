from Packages.tkinter import *
from Classes.ExtensionMethods import ExtensionMethods

class AdminGUI(object):
    def __init__(self, controller):
        self.__controller = controller

    #Renders the window to show request from the Members for the user to Accept or Decline
    def RequestView(self, window):
        ExtensionMethods.ClearTkWindow(window)

        def _back():
            ExtensionMethods.Redirect("Home", "index", window)
        Button(window, text="Back", command=_back).pack()
        window.title("Home")
        warning = StringVar()
        Label(window, background='lightblue', textvariable=warning).pack()
        Label(window, text="Requested Items").pack()
        
        itemRequests = self.__controller.LoadRequests()
        
        for _itemRequest in itemRequests:
            def acceptEvent():
                resultBool = self.__controller.AcceptRequest(_itemRequest)
                if resultBool:
                    self.RequestView(window)
                    warning.set("Request has been accepted and item has been loaned")
                else:
                    warning.set("Request can't be fulfilled as there is not enough stock")

            def declineEvent():
                resultBool = self.__controller.DeclineRequest(_itemRequest)
                if resultBool:
                    self.RequestView(window)

            _title = _itemRequest.GetTitle()
            Label(window, background='lightblue', text=_title).pack()
            Button(window, text="Accept", width=10, height=2, command=acceptEvent).pack()
            Button(window, text="Decline", width=10, height=2, command=declineEvent).pack()
            
        window.mainloop()
        
    #Renders the window to show loans from the Members for the user to Return them
    def LoanedView(self, window):
        ExtensionMethods.ClearTkWindow(window)

        def _back():
            ExtensionMethods.Redirect("Home", "index", window)
        Button(window, text="Back", command=_back).pack()
        window.title("Home")
        warning = StringVar()
        Label(window, background='lightblue', textvariable=warning).pack()
        Label(window, text="Loaned Items").pack()
        
        loans = self.__controller.LoadLoans()

        for _loan in loans:
            def returnEvent():
                resultBool = self.__controller.ReturnedLoan(_loan)
                if resultBool:
                    self.LoanedView(window)

            _title = _loan.GetTitle()
            if _loan.IsOverdue():
                Label(window, background='red', text=_title).pack()
            else:
                Label(window, background='lightblue', text=_title).pack()
            Button(window, text="Returned", width=10, height=2, command=returnEvent).pack()  

        window.mainloop()

        
    #Renders the window to show the reports in the system to generate
    def LoanReportView(self, window):
        ExtensionMethods.ClearTkWindow(window)

        def _back():
            ExtensionMethods.Redirect("Home", "index", window)
        Button(window, text="Back", command=_back).pack()
        window.title("Reports")
        warning = StringVar()
        
        def loanReportGenerateEvent():
            resultBool = self.__controller.LoadLoanedReport()
            if resultBool:
                warning.set("Report generated and will be in you're Report Folder.")
            else:
                warning.set("There is currently no Loans within the system.")
                
        def requestReportGenerateEvent():
            resultBool = self.__controller.LoadRequestReport()
            if resultBool:
                warning.set("Report generated and will be in you're Report Folder.")
            else:
                warning.set("There is currently no Item Request within the system.")
                
        def stockReportGenerateEvent():
            resultBool = self.__controller.LoadStockReport()
            if resultBool:
                warning.set("Report generated and will be in you're Report Folder.")
            else:
                warning.set("Sorry, something went wrong when trying to generate report.")

        def memberReportGenerateEvent():
            resultBool = self.__controller.LoadMembersReport()
            if resultBool:
                warning.set("Report generated and will be in you're Report Folder.")
            else:
                warning.set("Sorry, something went wrong when trying to generate report.")


        Label(window, background='lightblue', text="Loan Report").pack()
        Button(window, text="Generate", width=10, height=2, command=loanReportGenerateEvent).pack()  
        Label(window, background='lightblue', text="Request Report").pack()
        Button(window, text="Generate", width=10, height=2, command=requestReportGenerateEvent).pack()  
        Label(window, background='lightblue', text="Stock Report").pack()
        Button(window, text="Generate", width=10, height=2, command=stockReportGenerateEvent).pack()  
        Label(window, background='lightblue', text="Members Report").pack()
        Button(window, text="Generate", width=10, height=2, command=memberReportGenerateEvent).pack()  
        Label(window, background='lightblue', textvariable=warning).pack()



        window.mainloop()


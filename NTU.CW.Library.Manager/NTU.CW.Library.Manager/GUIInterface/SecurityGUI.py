from Packages.tkinter import *
from Models.Security.User import User
from Classes.ExtensionMethods import ExtensionMethods
from Models.Security.SecurityType import SecurityType
from Modules.Security.AuthorizationManager import AuthorizationManager
import hashlib

class SecurityGUI(object):
    def __init__(self, controller):
        self.__controller = controller
        
    #Renders the window to show the login menu screen, presents a login button
    def loginRegisterMenu(self, window):
        ExtensionMethods.ClearTkWindow(window)

        window.title("Account Login") 

        Label(text="Welcome to the library system", width="300", height="2", font=("Calibri", 13)).pack() 
        ExtensionMethods.DefaultBlankSpace(window)
        
        def loginTest():
            self.__controller.LoginMenuRedirect(window)
        
        Button(text="Login", height="2", width="30", command=loginTest).pack() 
        ExtensionMethods.DefaultBlankSpace(window)
 
        window.mainloop() 

    
    #Renders the window to show the login with a username and password entry, for users to logon
    def loginMenu(self, window):
        ExtensionMethods.ClearTkWindow(window)
        
        window.title("Login")
        username = StringVar()
        password = StringVar()
        warning = StringVar()
 
        def loginCommand():
             _username = username.get()
             hashPWObj = hashlib.md5(password.get().encode())
             _password = hashPWObj.hexdigest()
             result = self.__controller.Login(_username, _password)
             if result:
                 warning.set("")
                 ExtensionMethods.Redirect("Home", "index", window)
                 pass
             else:
                 warning.set("Username or Password is wrong.")

        Label(window, text="Please enter details below").pack()
        
        ExtensionMethods.DefaultBlankSpace(window)
    
        username_lable = Label(window, text="Username")
        username_lable.pack()
 
        username_entry = Entry(window, textvariable=username)
        username_entry.pack()
   
        password_lable = Label(window, text="Password")
        password_lable.pack()
    
        password_entry = Entry(window, textvariable=password, show='*')
        password_entry.pack()
    
        Label(window, background='lightblue', textvariable=warning).pack()
        Button(window, text="Login", width=10, height=1, command=loginCommand).pack()
        
    #Renders the window to show the profile of the user passed through
    #If user null then it will render the currently logged in user
    def profile(self, window, user=None):
        if user is None:
            user = AuthorizationManager.userInstance
        ExtensionMethods.ClearTkWindow(window)
        def _back():
            ExtensionMethods.Redirect("Home", "index", window)
        Button(window, text="Back", command=_back).pack()
        ExtensionMethods.DefaultBlankSpace(window)
        window.title("Profile")

        username = StringVar()
        firstName = StringVar()
        lastName = StringVar()
        password = StringVar()
        resetPasswordInt = IntVar()
        warning = StringVar()

        username.set(user.GetUserName())
        firstName.set(user.GetFirstName())
        lastName.set(user.GetLastName())

        def resetPasswordCbEvent():
            _cb = resetPasswordInt.get()
            if _cb == 1:
                password_lable.pack()
                password_entry.pack()
                saveButton.pack_forget()
                saveButton.pack()
                warningLabel.pack_forget()
                warningLabel.pack()
            else:
                password_lable.pack_forget()
                password_entry.pack_forget()

        username_lable = Label(window, text="Username")
        username_lable.pack()
 
        username_entry = Entry(window, textvariable=username)
        username_entry.pack()

        firstName_lable = Label(window, text="First Name")
        firstName_lable.pack()
 
        firstName_entry = Entry(window, textvariable=firstName)
        firstName_entry.pack()

        
        lastName_lable = Label(window, text="Last Name")
        lastName_lable.pack()
 
        lastName_entry = Entry(window, textvariable=lastName)
        lastName_entry.pack()

        resetPasswordCb = Checkbutton(window, text="Reset Password", variable=resetPasswordInt, command=resetPasswordCbEvent)
        resetPasswordCb.pack()

        password_lable = Label(window, text="New Password")
        #password_lable.pack()
    
        password_entry = Entry(window, textvariable=password, show='*')
        #password_entry.pack()


        def saveDeailEvent():
            user.SetUserName(username.get())
            user.SetFirstName(firstName.get())
            user.SetLastName(lastName.get())
            _cb = resetPasswordInt.get()
            if _cb == 1:
                hashPWObj = hashlib.md5(password.get().encode())
                _password = hashPWObj.hexdigest()
                user.SetResetPassword(_password)
            resultBool = user.SaveDetails()
            if resultBool:
                warning.set("Details Saved.")
        
        #ExtensionMethods.DefaultBlankSpace(window)
        saveButton = Button(window, text="Save", command=saveDeailEvent)
        saveButton.pack()
        warningLabel = Label(window, background='lightblue', textvariable=warning)
        warningLabel.pack()

    
    #Renders the window to show entries for creating a new instance of User type Member to be added
    def AddNewMember(self, window, _id):
        ExtensionMethods.ClearTkWindow(window)
        def _back():
            ExtensionMethods.Redirect("Security", "Members", window)
        Button(window, text="Back", command=_back).pack()
        ExtensionMethods.DefaultBlankSpace(window)
        window.title("Profile")

        username = StringVar()
        firstName = StringVar()
        lastName = StringVar()
        password = StringVar()
        warning = StringVar()

        username_lable = Label(window,background='lightblue', text="Username")
        username_lable.pack()
 
        username_entry = Entry(window, textvariable=username)
        username_entry.pack()

        firstName_lable = Label(window,background='lightblue', text="First Name")
        firstName_lable.pack()
 
        firstName_entry = Entry(window, textvariable=firstName)
        firstName_entry.pack()

        
        lastName_lable = Label(window,background='lightblue', text="Last Name")
        lastName_lable.pack()
 
        lastName_entry = Entry(window, textvariable=lastName)
        lastName_entry.pack()

        password_lable = Label(window,background='lightblue', text="Password")
        password_lable.pack()
 
        password_entry = Entry(window, textvariable=password, show='*')
        password_entry.pack()


        def addUserEvent():
            _user = User(_id, 0, username.get(), firstName.get(), lastName.get())
            hashPWObj = hashlib.md5(password.get().encode())
            _password = str(hashPWObj.hexdigest()).lower()
            _user.SetDefaultPassword(_password)
            resultBool = _user.SaveDetails()
            if resultBool:
                warning.set("User Added.")
        
        ExtensionMethods.DefaultBlankSpace(window)
        Button(window, text="Add", width=10, height=1, command=addUserEvent).pack()
        Label(window, background='lightblue', textvariable=warning).pack()
        
    #Renders the window to show a list of users within the system
    def members(self, window):
        ExtensionMethods.ClearTkWindow(window)

        def _back():
            ExtensionMethods.Redirect("Home", "index", window)
        Button(window, text="Back", command=_back).pack()
        window.title("Home")
        Label(window, text="Members").pack()
        
        users = self.__controller.ListUsers()
        
        for _user in users:
            def editEvent(_userId):
                eventUser = [u for u in users if u.GetUserId() == _userId][0]
                self.profile(window, eventUser)

            _title = str("{0} - {1}".format(_user.GetTypeName(), _user.GetUserName()))
            Label(window, background='lightblue', text=_title).pack()
            
            if AuthorizationManager.userInstance._type == SecurityType.LIBRARIAN.value:
                userId = _user.GetUserId()
                Button(window, text="Edit", width=10, height=2, command = lambda i=userId: editEvent(i)).pack()

        def addUser():
            userTop = sorted(users, key = lambda i: (i.GetUserId()))[0]
            userIdentity = int(userTop.GetUserId()) + 1
            self.AddNewMember(window, userIdentity)

        if AuthorizationManager.userInstance._type == SecurityType.LIBRARIAN.value:
            ExtensionMethods.DefaultBlankSpace(window)
            Button(window, text="Add", width=10, height=2, command = addUser).pack()
            
        window.mainloop()


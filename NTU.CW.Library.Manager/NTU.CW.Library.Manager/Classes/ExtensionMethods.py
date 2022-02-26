import json
import csv

class ExtensionMethods(object):
    
    #Creates and returns an instance of ExceptionManager
    @staticmethod
    def GetExceptionManager():
        from Modules.Exception.ExceptionManager import ExceptionManager
        return ExceptionManager()
    
    #Opens the JSON file location passed through and returns it within an array
    @staticmethod
    def loadJSON(fileLocation):
        data = []
        try:
            with open(fileLocation) as json_file:
                data = json.load(json_file)
                json_file.close()
        except Exception as ex:
            ExtensionMethods.GetExceptionManager().handleException(ex)
        return data
    
    #Opens the CSV file location passed through and returns it within an array
    @staticmethod 
    def loadCSV(fileLocation):
        data = []
        with open(fileLocation) as csvfile:
            _reader = csv.reader(csvfile, delimiter=',')
            #headers
            headers = []
            _index = 0
            for row in _reader:
                if _index > 0:
                    if len(row) > 0 and len(row[0]) > 0:
                        _obj = {}
                        _hIndex = 0
                        for _header in headers:
                            _obj[_header] = row[_hIndex]
                            _hIndex+=1
                        data.append(_obj)
                else:
                     headers = row
                _index+=1
        return data
    
    #Redirect the window instance to a new controller and method
    @staticmethod
    def Redirect(route, view, window=None):
        from Classes.RouteConfig import RouteConfig
        routeControls = RouteConfig.SetupRoutes(list())
        controller = [x for x in routeControls if route in x._routes and x._view == view][0]
        getattr(controller._controller, controller._view)(window)

    #https://stackoverflow.com/questions/45905665/is-there-a-way-to-clear-all-widgets-from-a-tkinter-window-in-one-go-without-refe/45915006
    #Above is a reference for clearing down tkinter windows and all its elements
    @staticmethod
    def ClearTkWindow(window):
        from Packages.tkinter import Tk
        _list = window.winfo_children()
        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())
        for item in _list:
            item.pack_forget()
        ExtensionMethods.ResetTkWindow(window)

    #After clearing tkinter window, this will set the background and any other extra elements to default
    @staticmethod
    def ResetTkWindow(window):
        from Packages.tkinter import Tk
        window.configure(background='lightblue')

    #Returns a element which acts as a blank space
    @staticmethod
    def DefaultBlankSpace(window):
        from Packages.tkinter import Tk, Label
        Label(window, text="", background='lightblue').pack()

    #With the string key passed through, it will look at the DataStorageLocation config to get the file location to parse the data
    #Returns data array
    @staticmethod
    def LoadData(key):
        data = []
        _config = ExtensionMethods.loadJSON("./config.json")
        if _config is not None:
            _storagekey = ExtensionMethods.ConfigGetDataStorageLocation()
            dataStorages = _config[_storagekey]
            _dataStorages = [x for x in dataStorages if x["key"] == key]
            if len(_dataStorages) > 0:
                _dataStorage = _dataStorages[0]
                _type = str(_dataStorage["type"])
                _value = str(_dataStorage["value"])
                if _type == "csv":
                    data = ExtensionMethods.loadCSV(_value)
                elif _type == "json":
                    data = ExtensionMethods.loadJSON(_value)
                elif _type == "location":
                    data = _value
        return data
    
    #With the string key passed through, it will look at the DataStorageLocation config to get the value by the config
    #Returns string
    @staticmethod
    def ConfigGetValueByKey(key):
        _value = ""
        _config = ExtensionMethods.loadJSON("./config.json")
        if _config is not None:
            _storagekey = ExtensionMethods.ConfigGetDataStorageLocation()
            dataStorages = _config[_storagekey]
            _dataStorages = [x for x in dataStorages if x["key"] == key]
            if len(_dataStorages) > 0:
                _dataStorage = _dataStorages[0]
                _value = str(_dataStorage["value"])
        return _value
    
    #If the application is within UnitTesting, this returns another config key to test data
    #Returns string
    @staticmethod
    def ConfigGetDataStorageLocation():
        from Classes.RouteConfig import RouteConfig
        key = "DataStorageLocation"
        if RouteConfig.UnitTestState == 1:
            key = "UnitTestDataStorageLocation"
        return key
    
    #With the string key passed through, it will look at the AppSettings config to get the value by the config
    #Returns string
    @staticmethod
    def AppSettingGetValueByKey(key):
        _value = ""
        _config = ExtensionMethods.loadJSON("./config.json")
        if _config is not None:
            dataStorages = _config["AppSettings"]
            _dataStorages = [x for x in dataStorages if x["key"] == key]
            if len(_dataStorages) > 0:
                _dataStorage = _dataStorages[0]
                _value = str(_dataStorage["value"])
        return _value
    
    #Saves the jsonData within the file location passed through
    #returns bool
    @staticmethod
    def SaveJSON(fileLocation, jsonData):
        resultBool = False
        with open(fileLocation, 'w') as file:
            data = json.dump(jsonData, file)
            resultBool = True
            file.close()
        return resultBool
    
    #Saves the csvData within the file location passed through
    #returns bool
    @staticmethod
    def SaveCSV(fileLocation, csvData):
        resultBool = False
        keys = csvData[0].keys()
        with open(fileLocation, 'w') as file:
            writer = csv.DictWriter(file, keys)
            writer.writeheader()
            writer.writerows(csvData)
            resultBool = True
            file.close()
        return resultBool
    
    #Creates a CSV with csvData passed against the file location and filename
    #returns bool
    @staticmethod
    def CreateCSV(fileLocation, fileName, csvData):
        resultBool = False
        fullLocation = (fileLocation + '/' + fileName)
        keys = csvData[0].keys()
        with open(fullLocation, 'w') as file:
            writer = csv.DictWriter(file, keys)
            writer.writeheader()
            writer.writerows(csvData)
            resultBool = True
            file.close()
        return resultBool

    
    
    #Returns the user name logged in
    @staticmethod
    def GetUserName():
        from Modules.Security.AuthorizationManager import AuthorizationManager
        return AuthorizationManager.userInstance.GetUserName()
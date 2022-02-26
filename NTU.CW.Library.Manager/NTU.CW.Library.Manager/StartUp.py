import json
from Packages.tkinter import *
from Classes.ExtensionMethods import *
from Classes.RouteConfig import RouteConfig
from Modules.Exception.ExceptionPolicy import ExceptionPolicy
from Modules.Exception.ExceptionManager import ExceptionManager
from Controllers import *


# Default Method for startup to call into default controller
# @param window: {object} tkinter window
def invokeDefaultController(window):
    controller = [x for x in routeControls if x._default][0]
    getattr(controller._controller, controller._view)(window)
    


# Firsts function to be hit
# Sets up global tkinter window for application.
if __name__ == "__main__":
    RouteConfig.UnitTestState = 0
    routeControls = RouteConfig.SetupRoutes(list())
    _window = Tk()
    _window.geometry("1280x1050")
    invokeDefaultController(_window)



from Route.RouteControl import RouteControl
from Controllers.CatalogueController import CatalogueController
from Controllers.SecurityController import SecurityController
from Controllers.HomeController import HomeController
from Controllers.AdminController import AdminController

class RouteConfig(object):
    RouteControls = list()
    UnitTestState = 0

    #Sets up the routes for the application for redirecting from controllers
    @staticmethod
    def SetupRoutes(routeControls):
        catalogueController = CatalogueController()
        securityController = SecurityController()
        homeController = HomeController()
        adminController = AdminController()

        routeControls.append(
                RouteControl(False, ["Catalogue"], catalogueController, "index")
            )
        routeControls.append(
                RouteControl(False, ["Catalogue"], catalogueController, "Product")
            )
        routeControls.append(
                RouteControl(True, ["Security"], securityController, "loginRegisterMenu")
            )
        routeControls.append(
                RouteControl(False, ["Home"], homeController, "index")
            )
        routeControls.append(
                RouteControl(False, ["Security"], securityController, "Logout")
            )
        routeControls.append(
                RouteControl(False, ["Admin"], adminController, "Request")
            )
        routeControls.append(
                RouteControl(False, ["Admin"], adminController, "Loaned")
            )
        routeControls.append(
                RouteControl(False, ["Admin"], adminController, "LoanedReport")
            )
        routeControls.append(
                RouteControl(False, ["Security"], securityController, "Profile")
            )
        routeControls.append(
                RouteControl(False, ["Security"], securityController, "Members")
            )
        RouteControls = routeControls
        return routeControls

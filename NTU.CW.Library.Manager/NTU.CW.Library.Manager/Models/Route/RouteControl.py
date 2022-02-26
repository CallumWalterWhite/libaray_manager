#Class to hold information for reidrecting between controllers and views
class RouteControl(object):
    def __init__(self, default, routes, controller, view="index"):
        self._default = default
        self._routes = routes
        self._controller = controller
        self._view = view

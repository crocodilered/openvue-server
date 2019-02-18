import cherrypy


__all__ = ['IndexController']


class IndexController:

    @cherrypy.expose
    def index(self):
        pass

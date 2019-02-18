import cherrypy as cp
from mysql.connector.pooling import MySQLConnectionPool
from cherrypy.process import plugins


__all__ = ['DbPlugin']


class DbPlugin(plugins.SimplePlugin):
    def __init__(self, bus, config):
        plugins.SimplePlugin.__init__(self, bus)
        self.engine = None
        self._pool = MySQLConnectionPool(pool_size=32, **config)

    def start(self):
        self.bus.subscribe('before_request', self._create_connection)
        self.bus.subscribe('after_request', self._close_connection)
        self.bus.log('DB plugin STARTED')

    def stop(self):
        self.bus.unsubscribe('before_request', self._create_connection)
        self.bus.unsubscribe('after_request', self._close_connection)
        if self._pool:
            del self._pool
        self.bus.log('DB plugin STOPPED')

    def _create_connection(self):
        cp.request.db = self._pool.get_connection()

    def _close_connection(self):
        cp.request.db.close()
        del cp.request.db

import os
import cherrypy
from libs.tools.auth_tool import AuthTool
from libs.plugins.db_plugin import DbPlugin as DbPlugin
from libs.plugins.auth_plugin import AuthSessions as AuthSessionsPlugin

cherrypy.tools.auth = AuthTool()

from libs.controllers.index import IndexController
from libs.controllers.auth import AuthController
from libs.controllers.folder import FolderController
from libs.controllers.formular import FormularController
from libs.controllers.wiki import WikiController

root = IndexController()
root.auth = AuthController()
root.folder = FolderController()
root.formular = FormularController()
root.wiki = WikiController()

curr_dir = os.path.abspath(os.path.dirname(__file__))
conf_file = os.path.join(curr_dir, 'conf', 'server.conf')

application = cherrypy.tree.mount(root, '/', conf_file)

cherrypy.config.update(conf_file)

db_conf = application.config['Database']
DbPlugin(cherrypy.engine, {
    'host': db_conf['mysql.host'],
    'port': db_conf['mysql.port'],
    'user': db_conf['mysql.user'],
    'password': db_conf['mysql.password'],
    'database': db_conf['mysql.database']
}).subscribe()

AuthSessionsPlugin(cherrypy.engine).subscribe()

if __name__ == '__main__':
    cherrypy.engine.start()

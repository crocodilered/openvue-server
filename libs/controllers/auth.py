import cherrypy as cp
from libs.controllers.abstract import AbstractController


__all__ = ['AuthController']


class AuthController(AbstractController):
    """
    AuthSessions controller
    """

    ERROR_WRONG_CREDENTIALS = 3
    ERROR_SESSION_NOT_FOUND = 4

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    def index(self):
        """ Return user by given token """
        r = {'errorCode': self.ERROR_SESSION_NOT_FOUND}
        user = cp.tools.auth.get_user()
        if user:
            r['user'] = user.json
            r['errorCode'] = 0
        return r

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    def sign_in(self):
        """ Start user session """
        r = {'errorCode': self.ERROR_WRONG_METHOD}
        if cp.request.method == 'POST':
            params = cp.request.json
            email = params['email'] if 'email' in params else None
            password = params['password'] if 'password' in params else None
            if email and password:
                token, user = cp.tools.auth.sign_in(email, password)
                if token and user:
                    r['token'] = token
                    r['user'] = user.json
                    r['errorCode'] = 0
                else:
                    r['errorCode'] = self.ERROR_WRONG_CREDENTIALS
            else:
                r['errorCode'] = self.ERROR_WRONG_REQUEST
        return r

    @cp.expose
    @cp.tools.auth()
    @cp.tools.json_out()
    def sign_out(self):
        """ Drop user session """
        cp.tools.auth.sign_out()
        return {'errorCode': 0}

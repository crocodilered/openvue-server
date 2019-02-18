import cherrypy as cp
import bcrypt
import uuid
from libs.providers.user import UserProvider


__all__ = ['AuthTool']


class AuthTool(cp.Tool):
    """
    Auth tool for JSON requests.
    User have to give us a token each time he ask for data.
    """
    def __init__(self):
        cp.Tool.__init__(self, 'before_handler', self._authenticate)

    def _authenticate(self):
        if not self.get_user():
            raise cp.HTTPError(401, 'Unauthorized')

    def sign_in(self, email, password):
        r = None, None
        user = UserProvider.get_by_email(cp.request.db, email)
        if user and user.enabled and AuthTool.match_password(password, user.password):
            token = AuthTool.generate_token()
            cp.engine.publish('auth-sign_in', token, user)
            r = token, user
        return r

    def sign_out(self):
        token = self.get_token()
        cp.engine.publish('auth-sign_out', token)

    def get_token(self):
        r = None
        if hasattr(cp.request, 'json'):
            r = cp.request.json['token']
        return r

    def get_user(self):
        token = self.get_token()
        user = cp.engine.publish('auth-get_user', token).pop()
        return user

    @staticmethod
    def encode_password(password):
        password = str.encode(password, encoding='UTF-8')
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        return password_hash.decode('utf-8')

    @staticmethod
    def match_password(attempt, password):
        attempt = str.encode(attempt, encoding='UTF-8')
        password = str.encode(password, encoding='UTF-8')
        return bcrypt.checkpw(attempt, password)

    @staticmethod
    def generate_token():
        return str(uuid.uuid4())

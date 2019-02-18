from cherrypy.process import plugins


__all__ = ['AuthSessions']


class AuthSessions(plugins.SimplePlugin):
    def __init__(self, bus):
        plugins.SimplePlugin.__init__(self, bus)
        # TODO: Move it to database (alive on server restart, can be shared)
        # TODO: Move it to JWT
        self._sessions = {}

    def start(self):
        self.bus.subscribe('auth-sign_in', self.sign_in)
        self.bus.subscribe('auth-sign_out', self.sign_out)
        self.bus.subscribe('auth-get_user', self.get_user)
        self.bus.log('AuthPlugin plugin STARTED')

    def stop(self):
        self.bus.unsubscribe('auth-sign_in', self.sign_in)
        self.bus.unsubscribe('auth-sign_out', self.sign_out)
        self.bus.unsubscribe('auth-get_user', self.get_user)
        self.bus.log('Auth plugin STOPPED')

    def sign_in(self, token, user):
        self._sessions[token] = user

    def sign_out(self, token):
        if token in self._sessions:
            del self._sessions[token]

    def get_user(self, token):
        user = self._sessions[token] if token in self._sessions else None
        return user

"""
Represents user's data
"""
__all__ = ['UserModel', 'UserInvalidDataException']


class UserModel:

    ROLE_ADMIN = 1
    ROLE_USER = 2

    def __init__(self, id: int, role: int, email: str, password: str, enabled: bool=False, token: str=None):
        if email and password:
            self.id = id
            self.role = int(role)
            self.email = email
            self.password = password
            self.enabled = enabled
            self.token = token
            self._display_name = None  # TODO: Use DB field 'user.name' instead.
        else:
            raise UserInvalidDataException

    @property
    def json(self):
        """ Make it JSON serializable """
        return {
            'id': int(self.id),
            'role': int(self.role),
            'email': self.email,
            'displayName': self.display_name
        }

    @property
    def display_name(self):
        if not self._display_name:
            self._display_name = self.email.split('@')[0]
        return self._display_name

class UserInvalidDataException (Exception):
    pass

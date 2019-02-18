import cherrypy as cp


__all__ = ['AbstractController']


class AbstractController(object):
    """
    Base controller to rule them all.
    """
    ERROR_WRONG_METHOD = 1
    ERROR_WRONG_REQUEST = 2
    ERROR_ACCESS_DENIED = 3

    def req_method_post(controller):
        def test_req_method(self):
            if cp.request.method == 'POST':
                return controller(self)
            else:
                return {
                    'errorCode': AbstractController.ERROR_WRONG_REQUEST,
                    'errorMessage': 'HTTP method must be POST.'
                }
        return test_req_method

    def req_user_any(controller):
        def test_req_user(self):
            user = cp.tools.auth.get_user()
            if user:
                return controller(self)
            else:
                return {
                    'errorCode': AbstractController.ERROR_ACCESS_DENIED,
                    'errorMessage': 'This controller is for authorized users only.'
                }
        return test_req_user

    def req_user_admin(controller):
        def test_req_user(self):
            user = cp.tools.auth.get_user()
            if user and user.role == user.ROLE_ADMIN:
                return controller(self)
            else:
                return {
                    'errorCode': AbstractController.ERROR_ACCESS_DENIED,
                    'errorMessage': 'This controller is for admins only.'
                }
        return test_req_user

    # Decorator
    def json_params(params_list):
        def wrapper(func):
            def wrapped_func(self):
                if isinstance(params_list, list) and hasattr(cp.request, 'json'):
                    json = cp.request.json
                    for param in params_list:
                        if param not in json or not json[param]:
                            return {'error': AbstractController.ERROR_WRONG_REQUEST}
                    return func(self)
                else:
                    return {'error': AbstractController.ERROR_WRONG_REQUEST}
            return wrapped_func
        return wrapper

    def extract_params(self, params_list):
        if params_list:
            params = cp.request.json
            r = []
            for param_name in params_list:
                p = params[param_name] if param_name in params else None
                r.append(p)
            return r if len(r) > 1 else r[0]

"""
Контроллер для исполнителя
"""

import cherrypy as cp
from libs.controllers.abstract import AbstractController
from libs.providers.formular import FormularProvider
from libs.models.formular import FormularModel

__all__ = ['FormularController']


class FormularController(AbstractController):

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    def index(self):
        """ Не понятно пока что тут показывать """
        return {'errorCode': 0}

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    @AbstractController.req_method_post
    @AbstractController.req_user_any
    def create(self):
        """
        Исполнитель создает расшифровку (формуляр).
        Параметры:
        - folderId - папка с делом
        - title - заголовок
        """
        params = cp.request.json

        if 'folderId' in params:
            folder_id = params['folderId']
        else:
            return {'errorCode': self.ERROR_WRONG_REQUEST}

        if 'title' in params:
            title = params['title']
        else:
            return {'errorCode': self.ERROR_WRONG_REQUEST}

        formular = FormularModel(None, folder_id, title)
        FormularProvider.create(cp.request.db, formular)

        return {'errorCode': 0}

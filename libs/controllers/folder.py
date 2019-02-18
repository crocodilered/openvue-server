import cherrypy as cp
from libs.controllers.abstract import AbstractController
from libs.models.folder import FolderModel
from libs.providers.folder import FolderProvider


__all__ = ['FolderController']


class FolderController(AbstractController):

    @property
    def purgatory_conf(self):
        return cp.request.app.config['Purgatory']

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    @AbstractController.req_method_post
    def index(self):
        """ Return general info """
        return {
            'errorCode': 0,
            'count': FolderProvider.count(cp.request.db),
            'countAvailable': FolderProvider.count_available(cp.request.db),
            'countPurgatory': FolderProvider.count_purgatory(self.purgatory_conf)
        }

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    @AbstractController.req_method_post
    @AbstractController.req_user_any
    def list_by_user(self):
        """
        Список дел, так или иначе имеющих отношение к пользователю.

        Можно передать userId (в этом случае текущий пользователь должен быть супервизором).
        Если userId не передан, выдается информация о текущем пользователе.
        """
        params = cp.request.json
        user = cp.tools.auth.get_user()

        if 'userId' in params:
            if user.role == user.ROLE_ADMIN:
                user_id = params['userId']
            else:
                return {'errorCode': self.ERROR_ACCESS_DENIED}
        else:
            user_id = user.id

        folders = FolderProvider.list_by_user(cp.request.db, user_id)
        r = {'errorCode': 0}
        if folders:
            r['data'] = [folder.json for folder in folders]

        return r

    @cp.expose(['import'])
    @cp.tools.json_in()
    @cp.tools.json_out()
    @AbstractController.req_method_post
    @AbstractController.req_user_admin
    def import_folders(self):
        """ Import folders """
        r = {'errorCode': 0}
        user = cp.tools.auth.get_user()
        FolderProvider.import_folders(cp.request.db, self.purgatory_conf, user.id)
        return r

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    @AbstractController.req_method_post
    @AbstractController.req_user_any
    def apply_performer(self):
        """
        Назначить расшифровщика для дела
        Параметры:
        - id: идентификатор записи. Если не определен, выбирается самое "старое" дело.
        - performer: исполнитель. Если не определен, берется id текущего пользователя.
        """
        r = {'errorCode': 0}
        params = cp.request.json

        user = cp.tools.auth.get_user()
        if 'performer' in params:
            if user.role == user.ROLE_ADMIN:
                performer_id = params['performer']
            else:
                return {'errorCode': self.ERROR_ACCESS_DENIED}
        else:
            performer_id = user.id

        folder = None

        if 'id' in params:
            folder = FolderProvider.get(cp.request.db, params['id'])
        else:
            # Выбираем самую старую запись
            rows = FolderProvider.raw(cp.request.db, 'WHERE status = 0 ORDER BY updated LIMIT 1')
            if rows and len(rows) > 0:
                folder = rows[0]

        if folder:
            folder.performer_id = performer_id
            folder.status = FolderModel.STATUS_PERFORMING
            folder = FolderProvider.update(cp.request.db, folder)
            r['data'] = folder.json

        return r

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    @AbstractController.req_method_post
    @AbstractController.req_user_any
    def get(self):
        """ Информация о файлах в папке """
        r = {'errorCode': 0}
        params = cp.request.json
        if 'id' in params:
            folder_id = params['id']
            folder = FolderProvider.get(cp.request.db, folder_id, with_files_list=True, conf=self.purgatory_conf)
            r['data'] = folder.json
        else:
            r['errorCode'] = self.ERROR_WRONG_REQUEST
        return r

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    @AbstractController.req_method_post
    @AbstractController.req_user_any
    def update(self):
        r = {'errorCode': 0}
        params = cp.request.json
        if 'folder' in params:
            folder = FolderModel.from_json(params['folder'])
            folder = FolderProvider.update(cp.request.db, folder)  # Simply update data
            r['data'] = folder.json
        else:
            r['errorCode'] = self.ERROR_WRONG_REQUEST
        return r

    @cp.expose
    def photo(self, f, n):
        path = f + '/' + n
        file = FolderProvider.file(self.purgatory_conf, path)
        cp.response.headers['Content-Type'] = 'image/jpeg'
        return file

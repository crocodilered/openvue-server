import os
import shutil
from libs.models.folder import FolderModel
from libs.providers.formular import FormularProvider


__all__ = ['FolderProvider']


class FolderProvider:

    SQL_UPDATE = '''
        UPDATE folder SET
            performer_id = {performer_id},
            status = {status}
        WHERE id = {id}
    '''

    SQL_LIST_BY_USER = '''
        SELECT
            folder.id,
            folder.title,
            folder.creator_id,
            folder.performer_id,
            folder.created,
            folder.updated,
            folder.status,
            user_creator.name,
            user_performer.name
        FROM folder
        LEFT JOIN user AS user_creator ON folder.creator_id = user_creator.id
        LEFT JOIN user AS user_performer ON folder.performer_id = user_performer.id
        WHERE performer_id = {user_id} OR creator_id = {user_id} 
        ORDER BY title
        LIMIT 1000 
    '''

    @staticmethod
    def count(conn, dt=None):
        """ Количество дел, зарегистрированных в БД """
        r = 0
        if conn:
            cur = conn.cursor()
            sql = 'SELECT COUNT(*) FROM folder'
            if dt:
                sql += ' WHERE updated >= "%s"' % dt
            cur.execute(sql)
            row = cur.fetchone()
            if row:
                r = row[0]
        return r

    @staticmethod
    def count_available(conn, dt=None):
        """ Количество дел, зарегистрированных в БД """
        r = 0
        if conn:
            cur = conn.cursor()
            sql = 'SELECT COUNT(*) FROM folder WHERE status = 0'
            if dt:
                sql += ' AND updated >= "%s"' % dt
            cur.execute(sql)
            row = cur.fetchone()
            if row:
                r = row[0]
        return r

    @staticmethod
    def count_purgatory(conf):
        """ Количество дел, загруженных на сервер, но не зарегистрированных в БД """
        r = 0
        if conf and 'purgatory.upload_dir' in conf:
            for root, dirs, files in os.walk(conf['purgatory.upload_dir']):
                for dir_name in dirs:
                    # os.path.join(i)
                    r += 1
        return r

    @staticmethod
    def list_purgatory(conf):
        """ Список дел, загруженных на сервер, но не зарегистрированных в БД """
        r = None
        if conf and 'purgatory.upload_dir' in conf:
            r = []
            for root, dirs, files in os.walk(conf['purgatory.upload_dir']):
                for dir_name in dirs:
                    # os.path.join(i)
                    r.append(dir_name)
        return r

    @staticmethod
    def get_photos(conf, folder):
        """ Список файлов в деле, зарегистрированном в БД """
        r = None
        if conf and 'purgatory.import_dir' in conf:
            r = []
            path = os.path.join(conf['purgatory.import_dir'], folder)
            for root, dirs, files in os.walk(path):
                for file_name in files:
                    # os.path.join(i)
                    r.append(file_name)
        return r

    @staticmethod
    def import_folders(conn, conf, creator_id):
        """ Зарегистрировать загруженные на сервер дела в БД """
        if conn and conf and 'purgatory.upload_dir' in conf and 'purgatory.import_dir' in conf:
            uploaded_folders = FolderProvider.list_purgatory(conf)
            if uploaded_folders:
                # insert info to database
                cur = conn.cursor()
                values = []
                for title in uploaded_folders:
                    values.append('("{0}", {1})'.format(title, creator_id))
                sql = 'INSERT INTO folder (title, creator_id) VALUES ' + ', '.join(values)
                cur.execute(sql)
                conn.commit()
                # move folders on disk
                src = conf['purgatory.upload_dir']
                dst = conf['purgatory.import_dir']
                for title in uploaded_folders:
                    shutil.move(os.path.join(src, title), os.path.join(dst, title))

    @staticmethod
    def list_by_user(conn, user_id):
        """ Список дел для выбранного пользователя (он может быть создателем или исполнителем) """
        r = None
        if conn:
            cur = conn.cursor()
            sql = FolderProvider.SQL_LIST_BY_USER.format(user_id=user_id)
            cur.execute(sql)
            rows = cur.fetchall()
            r = [FolderModel.from_row(row) for row in rows]
        return r

    @staticmethod
    def get(conn, folder_id, **params):
        folder = None
        records = FolderProvider.raw(conn, 'WHERE id = {}'.format(folder_id))
        if records:
            folder = records.pop()
            if 'with_files_list' in params and 'conf' in params and 'purgatory.import_dir' in params['conf']:
                # append files list
                folder.photos = FolderProvider.get_photos(params['conf'], folder.title)
            folder.formulars = FormularProvider.list(conn, folder_id)
        return folder

    @staticmethod
    def raw(conn, sql_where):
        """ Raw sql """
        r = None
        if conn and sql_where:
            cur = conn.cursor()
            sql = '''
                SELECT
                    id, title, creator_id, performer_id, created, updated, status 
                FROM
                    folder 
            ''' + sql_where
            cur.execute(sql)
            r = []
            for row in cur.fetchall():
                r.append(FolderModel.from_row(row))
        return r

    @staticmethod
    def update(conn, folder: FolderModel):
        r = None
        if conn and folder:
            cur = conn.cursor()
            sql = FolderProvider.SQL_UPDATE.format(**folder.json)
            cur.execute(sql)
            conn.commit()
            r = FolderProvider.get(conn, folder.id)
        return r

    @staticmethod
    def file(conf, path):
        """ Возвращает файл из файла folder/folder/filename """
        if 'purgatory.import_dir' in conf and path:
            full_path = os.path.join(conf['purgatory.import_dir'], path)
            f = open(full_path, 'rb')
            d = f.read()
            f.close()
            return d

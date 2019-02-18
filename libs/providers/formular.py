from libs.models.formular import FormularModel


__all__ = ['FormularProvider']


class FormularProvider:

    SQL_CREATE = '''
        INSERT INTO formular (
            folder_id,
            title
        ) VALUES (
            {folder_id},
            "{title}"
        )
    '''

    SQL_LIST = '''
        SELECT
            id,
            folder_id,
            title,
            created,
            updated
        FROM formular
        WHERE
            folder_id = {folder_id}
        ORDER BY
            title
    '''

    @staticmethod
    def create(conn, formular: FormularModel):
        cur = conn.cursor()
        sql = FormularProvider.SQL_CREATE.format(**formular.json)
        try:
            cur.execute(sql)
            conn.commit()
            return conn.insert_id()
        except:
            pass

    @staticmethod
    def list(conn, folder_id):
        cur = conn.cursor()
        sql = FormularProvider.SQL_LIST.format(folder_id=folder_id)
        cur.execute(sql)
        rows = cur.fetchall()
        r = None
        if rows:
            r = []
            for row in rows:
                r.append(FormularModel.from_row(row))
        return r

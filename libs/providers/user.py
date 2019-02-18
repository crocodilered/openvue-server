from libs.models.user import User


class UserProvider:

    @staticmethod
    def get_by_email(conn, email: str=None):
        r = None
        if conn and email:
            cur = conn.cursor()
            sql = 'SELECT id, role, email, password, enabled FROM user WHERE LOWER(email) = "%s"' % email.lower()
            cur.execute(sql)
            row = cur.fetchone()
            if row:
                r = User(row[0], row[1], row[2], row[3], row[3])
        return r

"""
Add and delete user
"""

import sys
import os
import re
import mysql.connector
from libs.tools.auth_tool import AuthTool


def init_connection():
    conf_file = open(os.path.join('..', 'conf', 'server.conf'), 'r')
    conf_data = conf_file.read()
    conf_file.close()

    m = re.search('mysql\.host = \'(.+?)\'', conf_data)
    mysql_host = m.group(1) if m else None

    m = re.search('mysql\.port = (\d+?)\n', conf_data)
    mysql_port = m.group(1) if m else None

    m = re.search('mysql\.user = \'(.+?)\'', conf_data)
    mysql_user = m.group(1) if m else None

    m = re.search('mysql\.password = \'(.+?)\'', conf_data)
    mysql_password = m.group(1) if m else None

    m = re.search('mysql\.database = \'(.+?)\'', conf_data)
    mysql_database = m.group(1) if m else None

    if mysql_host and mysql_port and mysql_user and mysql_password and mysql_database:
        return mysql.connector.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database)
    else:
        return None


def create_user(connection, role, email, password, name):
    role = 1 if role == 'admin' else 2
    encoded_password = AuthTool.encode_password(password)
    sql = '''INSERT INTO user (
        email,
        password,
        enabled,
        name,
        role
    ) VALUES (
        "{email}",
        "{password}",
        "1",
        "{name}",
        "{role}"
    )'''
    cursor = connection.cursor()
    cursor.execute(sql.format(role=role, email=email, password=encoded_password, name=name))
    print('User created.')


def set_user_status(connection, email, status=False):
    enabled = '1' if status else '0'
    sql = 'UPDATE user SET enabled = "{enabled}" WHERE email = "{email}"'
    cursor = connection.cursor()
    cursor.execute(sql.format(email=email, enabled=enabled))
    status_str = 'enabled' if status else 'disabled'
    print('User status set to ' + status_str + '.')


if __name__ == '__main__':

    usage_note = '''Usage:
user create {role:admin|regular} {email} {password} {lastname_firstname}
user enable {email}
user disable {email}'''

    args = sys.argv
    if len(args) == 1:
        print(usage_note)
        exit(1)

    connection = init_connection()
    if not connection:
        print('Error: mysql connection not initialized.')
        exit(2)

    if args[1] == 'create':
        # Create user
        if len(args) >= 6:
            user_role = args[2]
            user_email = args[3]
            user_password = args[4]
            user_name = args[5].replace('_', ' ')
            create_user(connection, user_role, user_email, user_password, user_name)
        else:
            print('Not enough arguments.\n\n' + usage_note)

    elif args[1] == 'enable':
        # Enable user
        if len(args) >= 3:
            user_email = args[2]
            set_user_status(connection, user_email, True)
        else:
            print('Not enough arguments.\n\n' + usage_note)

    elif args[1] == 'disable':
        # Disable user
        if len(args) >= 3:
            user_email = args[2]
            set_user_status(connection, user_email, False)
        else:
            print('Not enough arguments.\n\n' + usage_note)

    connection.commit()
    connection.close()

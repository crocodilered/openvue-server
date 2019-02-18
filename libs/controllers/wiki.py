import cherrypy as cp
import re
import requests
from libs.controllers.abstract import AbstractController
from libs.models.formular import FormularModel
from libs.providers.formular import FormularProvider


__all__ = ['WikiController']


class WikiController(AbstractController):

    SESSION = requests.session()

    @property
    def wiki_url(self):
        return cp.request.app.config['Wiki']['wiki.url']

    @property
    def api_url(self):
        return cp.request.app.config['Wiki']['wiki.url'] + 'api.php'

    def get_token(self, type='csrf'):
        """ Get token of given type from wiki """
        params = {
            'action': 'query',
            'format': 'json',
            'meta': 'tokens',
            'type': type
        }
        resp = self.SESSION.get(url=self.api_url, params=params)
        data = resp.json()
        token_name, token_value = type + 'token', ''
        if 'query' in data and 'tokens' in data['query'] and token_name in data['query']['tokens']:
            token_value = data['query']['tokens'][token_name]
        if len(token_value) > 3:
            return token_value
        else:
            return None

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    def csrf_token(self):
        token = self.get_token('csrf')
        if token:
            return {'token': token}
        else:
            return {'errorCode': 'no-token-given'}

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    @AbstractController.req_method_post
    def login(self):
        """ Login user to wiki """
        params = cp.request.json
        if 'username' not in params or 'password' not in params:
            return {'errorCode': 'no-params-given'}

        username, password = params['username'], params['password']

        login_token = self.get_token('login')
        if not login_token:
            return {'errorCode': 'no-login-token'}

        params = {
            'action': 'clientlogin',
            'format': 'json',
            'username': username,
            'password': password,
            'logintoken': login_token,
            'loginreturnurl': self.wiki_url
        }
        resp = self.SESSION.post(url=self.api_url, data=params)
        data = resp.json()
        if data['clientlogin']['status'] == 'PASS':
            return {'errorCode': 0}
        else:
            return {'errorCode': 'unknown-error'}

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    @AbstractController.json_params(['folderId', 'title'])
    def create_page(self):
        # Get token
        csrf_token = self.get_token()
        if not csrf_token:
            return {'errorCode': 'user-not-logged-in'}

        folder_id, page_title = self.extract_params(['folderId', 'title'])

        page_text = '''{{Шаблон:Формуляр
|источники данных=ГА РФ, архивно-следственное дело
}}

[[Категория:Электронная Книга памяти Москвы и Московской области]]
[[Категория:Москва и Московская обл.]]

==Биография==
        '''

        # Create page
        params = {
            'action': 'edit',
            'format': 'json',
            'title': page_title,
            'text': page_text,
            'tags': 'openvue',
            'summary': 'Automated creation.',
            'recreate': True,
            'createonly': True,
            'token': csrf_token
        }
        resp = self.SESSION.post(url=self.api_url, data=params)
        data = resp.json()

        if 'edit' in data and 'title' in data['edit']:
            formular = FormularModel(None, folder_id, page_title, FormularModel.STATUS_PERFORMING)
            FormularProvider.create(cp.request.db, formular)
            return {
                'page_title': data['edit']['title']
            }
        else:
            return {
                'errorCode': 'unknown'
            }

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    @AbstractController.json_params(['folderId', 'title'])
    def update_page(self):
        # Get token
        csrf_token = self.get_token()
        if not csrf_token:
            return {'errorCode': 'user-not-logged-in'}

        folder_id, page_title = self.extract_params(['folderId', 'title'])

        # Get page content
        # http://ru1.openlist.wiki/api.php?action=OlFormular&command=dump&title=R4
        resp = self.SESSION.post(url=self.api_url, data={
            'action': 'OlFormular',
            'format': 'json',
            'command': 'dump',
            'title': page_title
        })
        data = resp.json()
        page_text = data['page']

        # Источник данных - ГА РФ, архивно-следственное дело
        m = re.search('\|источники данных=(.+)?ГА РФ, архивно-следственное дело(.+)?\n', page_text, re.I)
        if not m:
            page_text = re.sub('\|источники данных=', '|источники данных=ГА РФ, архивно-следственное дело; ', page_text)

        # Категории: Электронная Книга памяти Москвы и Московской области; Москва и Московская обл.; Открытый список
        categories_text = '''
[[Категория:Электронная Книга памяти Москвы и Московской области]]
[[Категория:Москва и Московская обл.]]
[[Категория:Открытый список]]'''
        page_text = re.sub('}}', '}}\n\n' + categories_text, page_text)

        # Create page
        params = {
            'action': 'edit',
            'format': 'json',
            'title': page_title,
            'text': page_text,
            'tags': 'openvue',
            'summary': 'Automated updating.',
            'token': csrf_token
        }
        resp = self.SESSION.post(url=self.api_url, data=params)
        data = resp.json()

        if 'edit' in data and 'title' in data['edit']:
            formular = FormularModel(None, folder_id, page_title)
            FormularProvider.create(cp.request.db, formular)
            return {
                'page_title': data['edit']['title']
            }
        else:
            return {
                'errorCode': 'unknown'
            }

""" Mihoyo daily check-in api client """
import re

from requests import Session as _Session

from .data import URL, EVENT


class Client:
    """ Mihoyo API client """
    _user: dict = None
    _session: _Session = None

    def __init__(self, token: str = None, ac_id: int = None, uuid: str = None):
        """ Initialize API session """
        if not isinstance(token, (str,)):
            raise TypeError(
                f'token: Expected <str>, got {type(token).__name__}')

        if not re.match(r'^[0-9a-zA-Z]+$', token):
            raise ValueError(f'token: Invalid token "{token}"')

        if not isinstance(uuid, (str,)):
            raise TypeError(
                f'uuid: Expected <str>, got {type(token).__name__}')

        if not re.match(r'^[0-9a-z]{8}(-[0-9a-z]{4}){3}-[0-9a-z]{12}$', uuid):
            raise ValueError(f'uuid: Invalid UUID "{uuid}"')

        if not isinstance(ac_id, (int,)):
            raise TypeError(
                f'ac_id: Expected <str>, got {type(ac_id).__name__}')

        self._session = _Session()
        self._session.cookies.update({
            'cookie_token': str(token),
            'account_id': str(ac_id),
            '_MHYUUID': str(uuid),
            'mi18nLang': 'en-us'
        })
        self._session.headers.update({
            'DNT': '1',
            'Sec-GPC': '1',
            'Pragma': 'no-cache',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Cache-Control': 'no-cache',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://webstatic-sea.mihoyo.com',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://webstatic-sea.mihoyo.com/'
        })

    def _call(self, method, url, *args, **kwargs):
        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params']['lang'] = 'en-us'
        _data = self._session.request(method, url, *args, **kwargs)
        if _data and _data.status_code == 200:
            _data = _data.json()

        if _data['retcode'] == 0:
            return _data['data']
        return None

    @property
    def user(self):
        """ User Info """
        if not self._user:
            self._user = self._call('GET', URL.format('info'),
                                    params={'act_id': EVENT})
        return self._user

    @property
    def checked_in(self):
        """ Did check-in today? """
        return self.user.get('is_sign', None)

    @property
    def days(self):
        """ Total days checked-in """
        return self.user.get('total_sign_day', -1)

    def check_in(self):
        """ Check-in now """
        data = self._call('POST', URL.format('sign'),
                          json={'act_id': EVENT})
        if data and data['code'] == 'ok':
            self._user = None
            return True
        return False

# vim: ft=python3:ts=4:et:

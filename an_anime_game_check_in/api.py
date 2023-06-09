""" An Anime Game daily check-in api client """
import re
from enum import Enum
from time import sleep
from random import randrange
from requests import Session as __Session


def __b64d__(arg):
    """ Decode Base64 """
    from base64 import standard_b64decode as b64decode
    return b64decode(arg.encode()).decode() if isinstance(arg, (str,)) else arg


def __b64e__(arg):
    from base64 import standard_b64encode as b64encode
    return b64encode(arg.encode()).decode() if isinstance(arg, (str,)) else arg


class __CheckInMetaClass(type):
    __data: dict = None

    @property
    def _CheckIn__data(cls):
        if not cls.__data:
            from toml import load as load_toml
            from datetime import datetime as date
            from os import path
            file = path.join(path.dirname(__file__), 'games.toml')
            with open(file, encoding="utf8") as file:
                data = load_toml(file)
                cls.__data = {}
                for game, info in data.items():
                    cls.__data[game] = {}
                    for key, val in info.items():
                        cls.__data[game][key] = __b64d__(val)
        return cls.__data


class Games(Enum):
    KENJIN = 'KenJin'
    BOUGAI = 'BouGai3'
    SUTAAREIRU = 'SutaaReiru'


class Session(__Session):
    URL = __b64d__(
        'aHR0cHM6Ly9zZy17ZG9tYWlufS1hcGkuaG95b2xhYi5jb20ve3Jvb3R9L3tiYXNlfS97e319')

    def __init__(self, token: str, login: str, acid: int, uuid: str, **kwargs):
        if not isinstance(token, (str,)):
            raise TypeError(
                f'token: Expected <str>, got {type(token).__name__}')
        if not isinstance(login, (str,)):
            raise TypeError(
                f'token: Expected <str>, got {type(login).__name__}')
        if not isinstance(uuid, (str,)):
            raise TypeError(
                f'uuid: Expected <str>, got {type(uuid).__name__}')
        if not isinstance(acid, (int,)):
            raise TypeError(
                f'ac_id: Expected <str>, got {type(ac_id).__name__}')

        if not re.match(r'^[0-9a-zA-Z]+$', token):
            raise ValueError(f'token: Invalid token "{token}"')
        if not re.match(r'^[0-9a-zA-Z]+$', login):
            raise ValueError(f'token: Invalid login token "{login}"')
        if not re.match(r'^[0-9a-z]{8}(-[0-9a-z]{4}){3}-[0-9a-z]{12}$', uuid):
            raise ValueError(f'uuid: Invalid UUID "{uuid}"')

        super().__init__()
        self.cookies.update({
            'cookie_token': str(token),
            'account_id':   str(acid),
            'ltuid':        str(acid),
            'ltoken':       str(login),
            '_MHYUUID':     str(uuid),
            'mi18nLang': 'en-us'
        })
        self.cookies.update(kwargs)
        self.headers.update({
            'DNT': '1',
            'Sec-GPC': '1',
            'Pragma': 'no-cache',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Cache-Control': 'no-cache',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'en-US,en;q=0.5',
            'x-rpc-device_id': str(uuid),
            'x-rpc-lang': 'en',
            'Origin': __b64d__('aHR0cHM6Ly9hY3QuaG95b2xhYi5jb20='),
            'Accept': 'application/json, text/plain, */*',
            'Referer': __b64d__('aHR0cHM6Ly9hY3QuaG95b2xhYi5jb20v')
        })

    def get(self, game, path, data={}, *args, **kwargs):
        return self.ask('GET', game, path, params=data, *args, **kwargs)

    def post(self, game, path, data={}, *args, **kwargs):
        return self.ask('POST', game, path, json=data, *args, **kwargs)

    def test(self):
        url = self.URL.replace(__b64d__("c2cte2RvbWFpbn0tYXBp"), __b64d__("YXBpLWFjY291bnQtb3M=")).format(
            root='auth', base='api'
        ).format(__b64d__("Z2V0VXNlckFjY291bnRJbmZvQnlMVG9rZW4="))
        from time import time as epoch_now
        rsp = self.request('GET', url, params={
            't': int(epoch_now())
        })
        if rsp.ok and rsp.headers.get('Content-Type', 'text/plain') == 'application/json':
            rsp = rsp.json()
        return rsp['data'] if rsp['message'] == 'OK' else None

    def redeem(self, game, code):
        pass
        self.ask('GET', game, '')

    def ask(self, method, game, path, root='event', **kwargs):
        data = {}
        if 'params' in kwargs:
            data = kwargs.get('params')
        elif 'json' in kwargs:
            data = kwargs.get('json')
        else:
            kwargs.update({'params': data})

        data.update({
            'lang': 'en-us',
            'act_id': game['id']
        })

        url = self.URL.format(root=root, **game).format(path)
        _data = self.request(method, url, **kwargs)
        if _data and _data.status_code == 200:
            _data = _data.json()
        if _data['retcode'] == 0:
            sleep(randrange(1, 4))
            return _data['data'] or _data['retcode'] == 0
        return None


class CheckIn(metaclass=__CheckInMetaClass):
    """ A Certain Anime Game Web Event API client """

    __user: dict = None
    __user_makeup: dict = None
    __session: Session = None
    __game: dict = None
    __tasks: list = None

    def __init__(self, game: Games, session: Session):
        if not isinstance(game, (Games,)):
            raise TypeError(
                f'game: Expected <{Games}>, got {type(game).__name__}')

        if not isinstance(session, (Session,)):
            raise TypeError(
                f'session: Expected <{Session}>, got {type(session).__name__}')

        self.__session = session
        self.__game = CheckIn.__data.get(game.name)

    def reset(self):
        self.__user = None
        self.__user_makeup = None

    @property
    def supports_makeup(self):
        return self.__game.get('makeup_tasks', True)

    @property
    def makeup_tasks(self):
        if not self.supports_makeup:
            return [False]

        if not self.__tasks:
            ret = {}
            tasks = self.__session.get(
                self.__game, 'task/list').get('list', [])
            for task in tasks:
                ret.update({task['id']: task['status'] == 'TT_Award'})
            self.__tasks = ret
        return self.__tasks

    def makeup_claim(self, task):
        def ask(x): return self.__session.post(
            self.__game, x, data={'id': task})
        return ask('task/complete') and ask('task/award')

    @property
    def __makeup_info(self):
        if not self.__user_makeup:
            self.__user_makeup = self.__session.get(self.__game, 'resign_info')
        return self.__user_makeup or {}

    @property
    def can_makeup(self):
        def get(x): return self.__makeup_info.get(x)
        def alt(x, y): return self.__makeup_info.get(x, y)
        return all([
            get('resign_cnt_daily') < get('resign_limit_daily'),
            get('resign_cnt_monthly') < get('resign_limit_monthly'),
            get('sign_cnt_missed') > 0
        ])

    @property
    def missed(self):
        return self.__makeup_info.get('sign_cnt_missed', 0)

    def makeup(self):
        data = self.__session.post(self.__game, 'resign')
        return bool(data and data['message'] == '')

    @property
    def user(self):
        """ User Info """
        if not self.__user:
            self.__user = self.__session.get(self.__game, 'info')
        return self.__user or {}

    @property
    def done(self):
        """ Did check-in today? """
        return self.user.get('is_sign', False)

    @property
    def name(self):
        """ Get game name """
        return self.__game.get('name')

    @property
    def days(self):
        """ Total days checked-in """
        return self.user.get('total_sign_day', -1)

    def now(self):
        """ Check-in now """
        data = self.__session.post(self.__game, 'sign')
        return bool(data and data['code'] == 'ok')

# vim: ft=python3:ts=4:et:

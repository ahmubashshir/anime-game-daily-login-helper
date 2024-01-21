import sys
from base64 import standard_b64decode

# base url
_str_url = 'aHR0cHM6Ly9zZy17ZG9tYWlufS1hcGkuaG95b2xhYi5jb20ve3Jvb3R9L3tiYXNlfS97e319'
_str_game_frg = 'c2cte2RvbWFpbn0tYXBp'
_str_auth_frg = 'YXBpLWFjY291bnQtb3M='
_str_auth_prm = 'Z2V0VXNlckFjY291bnRJbmZvQnlMVG9rZW4='

# cookie names
_str_cn_tkn = 'Y29va2llX3Rva2Vu'
_str_cn_aid = 'YWNjb3VudF9pZA=='
_str_cn_uid = 'bHR1aWQ='
_str_cn_ltk = 'bHRva2Vu'
_str_cn_gid = 'X01IWVVVSUQ='
_str_cn_lng = 'bWkxOG5MYW5n'

# headers
_str_origin_url_v = 'aHR0cHM6Ly9hY3QuaG95b2xhYi5jb20='
_str_referer_v = 'aHR0cHM6Ly9hY3QuaG95b2xhYi5jb20v'
_str_h_rpc_n = 'eC1ycGMtZGV2aWNlX2lk'
_str_h_rpc_lng_n = 'eC1ycGMtbGFuZw=='


def __b64d__(name):
    """ Decode Base64 """
    if not f"_str_{name}" in globals():
        raise AttributeError(f"{name!r} not found in {__name__!r}")

    data = globals().get(f"_str_{name}")
    if isinstance(data, (str,)):
        data = globals()[f"_str_{name}"] = standard_b64decode(data.encode())

    return data.decode()


if sys.version_info >= (3, 7):
    def __getattr__(name: str) -> str:
        return __b64d__(name)
else:
    class strings:
        def __getattr__(name: str) -> str:
            return __b64d__(name)
    sys.modules[__name__] = strings()

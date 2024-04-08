import sys
from base64 import standard_b64decode, standard_b64encode

# base url
_str_url = 'aHR0cHM6Ly9zZy17ZG9tYWlufS1hcGkuaG95b2xhYi5jb20ve3Jvb3R9L3tiYXNlfS97e319'
_str_game_frg = 'c2cte2RvbWFpbn0tYXBp'
_str_auth_frg = 'YXBpLWFjY291bnQtb3M='
_str_auth_prm = 'Z2V0VXNlckFjY291bnRJbmZvQnlMVG9rZW4='

# cookie names
_str_cn_uuid = 'X01IWVVVSUQ='  # _MHYUUID
_str_cn_ltkn = 'bHRva2VuX3Yy'  # ltoken_v2
_str_cn_ctkn = 'Y29va2llX3Rva2VuX3Yy'  # cookie_token_v2
_str_cn_lmid = 'bHRtaWRfdjI='  # ltmid_v2
_str_cn_amid = 'YWNjb3VudF9taWRfdjI='  # account_mid_v2
_str_cn_ltid = 'bHR1aWRfdjI='  # ltuid_v2
_str_cn_acid = 'YWNjb3VudF9pZF92Mg=='  # account_id_v2

# headers
_str_origin_url_v = 'aHR0cHM6Ly9hY3QuaG95b2xhYi5jb20='
_str_referer_v = 'aHR0cHM6Ly9hY3QuaG95b2xhYi5jb20v'


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

    def b64enc(_str):
        return standard_b64encode(_str.encode()).decode()
else:
    class strings:
        def b64enc(_str):
            return standard_b64encode(_str.encode()).decode()

        def __getattr__(name: str) -> str:
            return __b64d__(name)
    sys.modules[__name__] = strings()

import sys
from base64 import standard_b64decode, standard_b64encode

# base url
_d_url = 'aHR0cHM6Ly9zZy17ZG9tYWlufS1hcGkuaG95b2xhYi5jb20ve3Jvb3R9L3tiYXNlfS97e319'
_d_game_frg = 'c2cte2RvbWFpbn0tYXBp'
_d_auth_frg = 'YXBpLWFjY291bnQtb3M='
_d_auth_prm = 'Z2V0VXNlckFjY291bnRJbmZvQnlMVG9rZW4='

# data keys
_d_gid = 'YWN0X2lk'

# cookie names
_d_cn_uuid = 'X01IWVVVSUQ='
_d_cn_ltkn = 'bHRva2VuX3Yy'
_d_cn_ctkn = 'Y29va2llX3Rva2VuX3Yy'
_d_cn_lmid = 'bHRtaWRfdjI='
_d_cn_amid = 'YWNjb3VudF9taWRfdjI='
_d_cn_ltid = 'bHR1aWRfdjI='
_d_cn_acid = 'YWNjb3VudF9pZF92Mg=='

# headers
_d_origin_url_v = 'aHR0cHM6Ly9hY3QuaG95b2xhYi5jb20='
_d_referer_v = 'aHR0cHM6Ly9hY3QuaG95b2xhYi5jb20v'

# api request paths

_d_tlist = 'dGFzay9saXN0'
_d_tdone = 'dGFzay9jb21wbGV0ZQ=='
_d_tprize = 'dGFzay9hd2FyZA=='
_d_authinfo = 'aW5mbw=='
_d_streak_recover = 'cmVzaWdu'
_d_commit = 'c2lnbg=='

# api response keys/vals
_d_tlist_key = 'bGlzdA=='
_d_tstatus = 'VFRfQXdhcmQ='
_d_rsinfo = 'cmVzaWduX2luZm8='
_d_streak = 'dG90YWxfc2lnbl9kYXk='

_d_is_claimed = 'aXNfc2lnbg=='
_d_missed_streak = 'c2lnbl9jbnRfbWlzc2Vk'
_d_scount = 'cmVzaWduX2NudF97fQ=='
_d_slimit = 'cmVzaWduX2xpbWl0X3t9'


def __b64d__(name):
    """ Decode Base64 """
    if not f"_d_{name}" in globals():
        raise AttributeError(f"{name!r} not found in {__name__!r}")

    data = globals().get(f"_d_{name}")
    if isinstance(data, (str,)):
        data = globals()[f"_d_{name}"] = standard_b64decode(data.encode())

    return data.decode()


def decode():
    for item in filter(lambda x: x.startswith('_d_'), globals()):
        print((lambda x: (x, __b64d__(x),))(item.removeprefix('_d_')))


def b64enc(_str):
    return standard_b64encode(_str.encode()).decode()


def encode():
    items = globals()
    for item in filter(lambda x: x.startswith('_s_'), items):
        print((lambda x: '{}  = \'{}\''.format(f'_d_{x}', b64enc(items[item])))(
            item.removeprefix('_s_')))


if sys.version_info >= (3, 7):
    def __getattr__(name: str) -> str:
        return __b64d__(name)
else:
    class strings:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

        def __getattr__(self, name: str) -> str:
            return __b64d__(name)

    sys.modules[__name__] = strings(
        decode=decode,
        b64enc=b64enc,
        encode=encode
    )

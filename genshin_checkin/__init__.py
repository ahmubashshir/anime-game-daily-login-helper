from os import environ as _ENV

from .api import Client as _Client


def main(token=None, uid=None):
    if not token:
        token = _ENV['MHYTOKEN']
    if not uid:
        uid = _ENV['MHYACID']
    client = _Client(token, uid)

    try:
        check_in = False
        if not client.checked_in:
            check_in = True

        if check_in and client.check_in():
            award = client.data['awards'][client.check_in_days]
            print(f'Checked in: Got {award["cnt"]}x {award["name"]}')
    except Exception as _e:
        print(_e)

# vim: ft=python3:ts=4:et:

from os import environ as _ENV

from .api import Client as _Client


def main(token=None, ac_id=None, uuid=None):
    if not token:
        token = _ENV['MHYTOKEN']
    if not ac_id:
        ac_id = int(_ENV['MHYACID'])
    if not uuid:
        uuid = _ENV['MHYUUID']
    client = _Client(token, ac_id, uuid)

    try:
        check_in = False
        if not client.checked_in:
            check_in = True

        if check_in and client.check_in():
            print(f'Checked in: {client.days} days streak')
        elif client.check_in:
            print(f'Already checked in: {client.days} days streak')
        else:
            raise RuntimeError("Failed to check in")
    except Exception as _e:
        print(_e)

# vim: ft=python3:ts=4:et:

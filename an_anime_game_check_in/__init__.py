""" An Anime Game Web Event Check-in bot """
from sys import exit
from os import environ as _ENV
from argparse import ArgumentParser

from .api import Games, CheckIn, Session
from .util import try_check_in


def main():
    """ The Main Method """

    parser = ArgumentParser()
    parser.add_argument("-i", "--id", type=int, help="Set User ID")
    parser.add_argument("-t", "--token", type=str, help="Set Token")
    parser.add_argument("-c", "--cookie", type=str, help="Set Cookie Token")
    parser.add_argument("-l", "--login", type=str, help="Set Log-in Token")
    parser.add_argument("-u", "--uuid", type=str, help="Set UUID")
    parser.add_argument("-g", "--games", nargs='+', type=Games,
                        help="Set Server Region")
    args = parser.parse_args()
    ac_id, token, cookie, login, uuid, games = args.id, args.token, args.cookie, args.login, args.uuid, args.games

    if not token:
        token = _ENV['TOKEN']
    if not cookie:
        cookie = _ENV['COOKIE']
    if not login:
        login = _ENV['LOGIN']
    if not ac_id:
        ac_id = int(_ENV['ACCOUNT'])
    if not uuid:
        uuid = _ENV['UUID']
    if not games:
        games = [Games(game.strip()) for game in _ENV['GAMES'].split(':')]

    session = Session(token, cookie, login, ac_id, uuid)
    try:
        info = session.test()
        print("""
Logged in Successfully as
    Account: {account_name}
    E-Mail : {email}
""".format(**info))
    except Exception as e:
        print(e)
        exit(5)

    statuses = {}

    for game in games:
        client = CheckIn(game, session)
        statuses[game] = True

        if try_check_in(client, 3):
            print(f'{client.name:>17s}: {client.days:>2d} days streak')
        else:
            print(f'{client.name:>17s}: Failed to check in')
            statuses[game] = False

        if not client.supports_makeup or client.missed == 0:
            continue

        if len(client.makeup_tasks) > 0 and not all(client.makeup_tasks.values()):
            for task, done in client.makeup_tasks.items():
                if not done:
                    if client.makeup_claim(task):
                        print(f'{client.name:>17s}: Claimed make up token')

        if client.can_makeup:
            if client.makeup():
                client.reset()
                print(f'{client.name:>17s}: Made up 1 missed check in')
                print(f'{client.name:>17s}: {client.days:>2d} days streak')
            else:
                print(f'{client.name:>17s}: Failed to make up missed check in')
                statuses[game] = False

    return (0 if all(statuses.values()) else 1)

# vim: ft=python3:ts=4:et:

""" An Anime Game Web Event Check-in bot """
from sys import exit
from os import environ as _ENV
from argparse import ArgumentParser

from .api import Games, CheckIn, Session


def main():
    """ The Main Method """

    parser = ArgumentParser()
    parser.add_argument("-i", "--id", type=int, help="Set User ID")
    parser.add_argument("-t", "--token", type=str, help="Set Token")
    parser.add_argument("-u", "--uuid", type=str, help="Set UUID")
    parser.add_argument("-g", "--games", nargs='+', type=Games,
                        help="Set Server Region")
    args = parser.parse_args()
    ac_id, token, uuid, games = args.id, args.token, args.uuid, args.games

    if not token:
        token = _ENV['TOKEN']
    if not ac_id:
        ac_id = int(_ENV['ACCOUNT'])
    if not uuid:
        uuid = _ENV['UUID']
    if not games:
        games = [Games(game.strip()) for game in _ENV['GAMES'].split(':')]

    session = Session(token, ac_id, uuid)
    try:
        session.test()
    except Exception as e:
        print(e)
        exit(5)

    statuses = {}

    for game in games:
        check_in = CheckIn(game, session)
        statuses[game] = True

        if check_in.done or not check_in.done and check_in.now():
            check_in.reset()
            print(f'{check_in.name:>17s}: {check_in.days:>2d} days streak')
        else:
            print(f'{check_in.name:>17s}: Failed to check in')
            statuses[game] = False

        if not check_in.supports_makeup:
            continue

        if len(check_in.makeup_tasks) > 0 and not all(check_in.makeup_tasks.values()):
            for task, done in check_in.makeup_tasks.items():
                if not done:
                    if check_in.makeup_claim(task):
                        print(f'{check_in.name:>17s}: Claimed make up token')

        if check_in.can_makeup:
            if check_in.makeup():
                check_in.reset()
                print(f'{check_in.name:>17s}: Made up 1 missed check in')
                print(f'{check_in.name:>17s}: {check_in.days:>2d} days streak')
            else:
                print(f'{check_in.name:>17s}: Failed to make up missed check in')
                statuses[game] = False

    exit(0 if all(statuses.values()) else 1)

# vim: ft=python3:ts=4:et:

from . import main
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-u", "--uid", type=int, help="Set UID")
    parser.add_argument("-t", "--token", type=str, help="Set Token")
    args = parser.parse_args()

    main(uid=args.uid, token=args.token)

# vim: ft=python3:ts=4:et:

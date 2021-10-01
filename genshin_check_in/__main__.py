from . import main
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-i", "--id", type=int, help="Set User ID")
    parser.add_argument("-t", "--token", type=str, help="Set Token")
    parser.add_argument("-u", "--uuid", type=str, help="Set UUID")
    args = parser.parse_args()

    main(ac_id=args.id, token=args.token, uuid=args.uuid)

# vim: ft=python3:ts=4:et:

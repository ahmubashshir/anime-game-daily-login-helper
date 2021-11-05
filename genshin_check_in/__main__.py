""" The main module """
from argparse import ArgumentParser

from . import main
from .api import Region

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-i", "--id", type=int, help="Set User ID")
    parser.add_argument("-t", "--token", type=str, help="Set Token")
    parser.add_argument("-u", "--uuid", type=str, help="Set UUID")
    parser.add_argument("-r", "--region", type=Region,
                        help="Set Server Region")
    args = parser.parse_args()

    main(ac_id=args.id, token=args.token, uuid=args.uuid, region=args.region)

# vim: ft=python3:ts=4:et:

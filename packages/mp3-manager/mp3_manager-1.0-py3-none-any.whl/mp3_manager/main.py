from argparse import ArgumentParser
from .mp3_manager import scan, edit


def cli():
    parser = ArgumentParser(
        prog="mp3",
        description="A CLI to manage Listo 502 mp3."
    )
    parser.add_argument(
        "-p", 
        "--path", 
        required=True, 
        type=str, 
        help="The path to listo 502 mp3.")
    subparsers = parser.add_subparsers()
    scan_parser = subparsers.add_parser("scan")
    scan_parser.set_defaults(func=scan)
    edit_parser = subparsers.add_parser("edit")
    edit_parser.add_argument("-csv", type=str, default=None)
    edit_parser.set_defaults(func=edit)
    args = parser.parse_args()
    print(args)
    args.func(args)
    
from argparse import ArgumentParser
import config


def main() -> None:
    parser = ArgumentParser()
    sub = parser.add_subparsers(required=True)
    conf = sub.add_parser("config", help="Read or modify the configs")
    config.setup_parser(conf)

    cost = sub.add_parser("cost")
    invoice = sub.add_parser("invoice")
    args = parser.parse_args()
    args.func(args)


main()

import os
from pathlib import Path
from typing import Dict
import json
import sys


XDG_CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME")) or Path("~/.config")
CONFIG_FILE: Path = XDG_CONFIG_HOME / ".infakt_cli"
CONFIG_ACTIONS = ["list", "add"]
CONFIG_KEYS = ["API_KEY"]


def setup_parser(parser):
    parser.set_defaults(func=dispatch)
    subconf = parser.add_subparsers()
    list_parser = subconf.add_parser("list")
    list_parser.set_defaults(conf_func=list_configs)
    add_parser = subconf.add_parser("add")
    add_parser.add_argument("config_key", choices=CONFIG_KEYS)
    add_parser.add_argument("config_value", type=str)
    add_parser.set_defaults(conf_func=add_config)


def dispatch(args):
    args.conf_func(args)


def add_config(args):
    conf = get_configs() or {}
    conf[args.config_key] = args.config_value
    save_configs(conf)
    print("Configs updated succesfully!")


def list_configs(args):
    conf = get_configs()
    if conf is None:
        print(
            f'No config found! Create it add {CONFIG_FILE} or use "config add <key> <value>".'
        )
        sys.exit(0)
    print(conf)


def get_configs() -> Dict[str, str]:
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def save_configs(c: Dict[str, str]):
    with open(CONFIG_FILE, "wt") as f:
        json.dump(c, f)

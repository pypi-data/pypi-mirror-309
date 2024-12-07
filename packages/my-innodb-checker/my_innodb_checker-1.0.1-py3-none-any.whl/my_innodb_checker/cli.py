"""
Cli entry module
"""

import argparse
import os
from argparse import ArgumentParser
from logging import getLogger
from typing import Callable, List, Optional, Union

from .constants import MyLogin
from .helpers import init_logger
from .mysqlsh import MysqlSh


def argument(*name_or_flags, **kwargs):
    """
    Argparse argument function
    """
    return (list(name_or_flags), kwargs)


def command(
    args: Optional[Union[Union[str, Callable], list]] = None,
    parent: Optional[ArgumentParser] = None,
    cmd_aliases: Optional[List[str]] = None,
) -> Callable:
    """
    Decorator for argument parser
    :param ArgumentParser parent: parent for arguments
    :param list[argument] args: unknow
    :param list[str] cmd_aliases: aliases for cli option
    """
    if cmd_aliases is None:
        cmd_aliases = []
    if args is None:
        args = []

    def decorator(func):
        parser = parent.add_parser(
            func.__name__.replace("_", "-"),
            description=func.__doc__,
            aliases=cmd_aliases,
        )
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)

    return decorator


def arguments() -> ArgumentParser:
    """
    Cli argument function
    """
    args = argparse.ArgumentParser()
    args.add_argument(
        "--log-level",
        help="log level, default: %(default)s",
        default="warning",
        type=str,
        choices=["warning", "info", "debug", "error", "critical"],
    )
    mysql = args.add_argument_group("Mysql")
    mysql.add_argument(
        "-H",
        "--host",
        help="host to connect, default: %(default)s",
        default="localhost",
        type=str,
    )
    mysql.add_argument(
        "-P",
        "--port",
        help="Port to use for connection, default: %(default)s",
        default=3306,
        type=int,
    )
    mysql.add_argument(
        "-U",
        "--user",
        help="Username for connection, default: %(default)s",
        default=os.getlogin(),
        type=str,
    )
    mysql.add_argument("--password", help="Password", type=str, default="")
    mysql.add_argument(
        "--defaults-file",
        help="Path to defaults file, default: %(default)s",
        default=os.path.join(os.environ["HOME"], ".my.cnf"),
        type=str,
    )
    return args


cli_args = arguments()
subargs = cli_args.add_subparsers(dest="cli")


def main() -> None:
    """
    Main function
    """
    parsed_args = cli_args.parse_args()
    if parsed_args.cli is None:
        cli_args.print_help()
        return
    init_logger(name="my_innodb_checker", level=parsed_args.log_level)
    _logger = getLogger("my_innodb_checker")
    _logger.info("Starting mychecker")
    parsed_args.func(parsed_args)


@command(
    parent=subargs,  # type: ignore
)
def check_cluster(args) -> None:
    """
    Cluster check using mysqlsh cli
    """
    logins: Union[str, MyLogin, None] = None
    if os.path.isfile(args.defaults_file):
        logins = args.defaults_file
    else:
        logins = {
            "user": args.user,
            "password": args.password,
            "host": args.host,
            "port": args.port,
        }
    mysqlsh = MysqlSh(logins=logins)
    mysqlsh.cluster_status()


@command(
    parent=subargs,  # type: ignore
)
def check_clusterset(args) -> None:
    """
    Cli command to check clusterset
    """
    logins: Union[str, MyLogin, None] = None
    if os.path.isfile(args.defaults_file):
        logins = args.defaults_file
    else:
        logins = {
            "user": args.user,
            "password": args.password,
            "host": args.host,
            "port": args.port,
        }
    mysqlsh = MysqlSh(logins=logins)
    mysqlsh.clusterset_status()

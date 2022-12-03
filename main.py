import argparse
import logging
import os
import sys

import constants
from commands.run import execute_run

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('commit-analysis')

# borrowed as a resolution from https://github.com/pre-commit/pre-commit/issues/217
os.environ.pop('__PYVENV_LAUNCHER__', None)


def add_command_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        'command', choices=constants.COMMANDS
    )


def parse_and_delegate(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    logger.info(args.command)
    if args.command == "run":
        execute_run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='commit-analysis')
    add_command_option(parser)
    parse_and_delegate(parser)
